#!/usr/bin/env python3

"""
Fyers MCP Server

A Model Context Protocol server for Fyers API integration providing:
- Authentication and token management
- Historical data retrieval
- Order management
- Profile and account details
- Position and holdings information

Requirements:
- fyers-apiv3
- mcp
- pyotp
- requests
"""

import base64
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs, urlparse
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass

import requests
from fyers_apiv3 import fyersModel
from mcp.server.fastmcp import FastMCP, Context
from pyotp import TOTP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

def setup_fyers_logging():
    """Setup Fyers API logging path from environment or disable it"""
    try:
        log_path = os.getenv('FYERS_LOG_PATH', os.devnull)
        os.environ['FYERS_LOG_FILE'] = log_path
        if log_path == os.devnull:
            print("✓ Fyers logging disabled", file=sys.stderr)
        else:
            print(f"✓ Fyers log path set to: {log_path}", file=sys.stderr)
    except Exception as e:
        print(f"⚠️  Warning: Could not setup Fyers logging: {e}", file=sys.stderr)

def validate_environment():
    """Check if all required environment variables are present"""
    required_vars = [
        'APP_CLIENT_ID', 'APP_SECRET_KEY', 'FYERS_USERNAME',
        'FYERS_TOTP_KEY', 'FYERS_PIN'
    ]
    
    missing_vars = []
    env_status = {}
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
            env_status[var] = "❌ MISSING"
        else:
            env_status[var] = "✅ SET"
    
    # Optional variable
    fyers_log_path = os.getenv('FYERS_LOG_PATH')
    env_status['FYERS_LOG_PATH'] = "✅ SET" if fyers_log_path else "⚠️  OPTIONAL (using default)"
    
    print("📋 Environment Variables Status:", file=sys.stderr)
    for var, status in env_status.items():
        print(f"   {var}: {status}", file=sys.stderr)
    
    if missing_vars:
        print(f"\n❌ Missing required environment variables: {missing_vars}", file=sys.stderr)
        print("💡 Please ensure all required variables are set in your MCP server configuration.", file=sys.stderr)
        return False
    
    print(f"\n✅ All {len(required_vars)} required environment variables are present", file=sys.stderr)
    return True

@dataclass
class AppContext:
    token_manager: 'FyersTokenManager'

class FyersTokenManager:
    """Manages Fyers authentication tokens with automatic refresh"""
    
    def __init__(self):
        # Get environment variables
        self.client_id = os.getenv('APP_CLIENT_ID')
        self.secret_key = os.getenv('APP_SECRET_KEY')
        self.redirect_uri = os.getenv('APP_REDIRECT_URI', 'https://127.0.0.1')
        self.username = os.getenv('FYERS_USERNAME')
        self.totp_key = os.getenv('FYERS_TOTP_KEY')
        self.pin = os.getenv('FYERS_PIN')
        
        # Session-based token storage (in memory)
        self._session_token = None
        self._token_timestamp = None
        self._token_expiry_hours = 24
        
        # Validate required environment variables
        required_vars = {
            'APP_CLIENT_ID': self.client_id,
            'APP_SECRET_KEY': self.secret_key,
            'FYERS_USERNAME': self.username,
            'FYERS_TOTP_KEY': self.totp_key,
            'FYERS_PIN': self.pin
        }
        
        missing_vars = [var for var, value in required_vars.items() if not value]
        if missing_vars:
            error_msg = f"Missing required environment variables: {missing_vars}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.info("FyersTokenManager initialized successfully")
    
    def totp(self, key: str) -> str:
        """Generate TOTP code for authentication"""
        try:
            totp = TOTP(key)
            return totp.now()
        except Exception as e:
            logger.error(f"Error generating TOTP: {e}")
            raise
    
    def store_token_in_session(self, token: str) -> None:
        """Store token in session memory with timestamp"""
        self._session_token = token
        self._token_timestamp = datetime.now()
        logger.info(f"Token stored in session at {self._token_timestamp}")
    
    def get_session_token(self) -> Optional[str]:
        """Get token from session memory if valid and not expired"""
        if not self._session_token or not self._token_timestamp:
            return None
        
        # Check if token is expired (24 hours)
        elapsed = datetime.now() - self._token_timestamp
        if elapsed.total_seconds() > (self._token_expiry_hours * 3600):
            logger.info("Session token expired, clearing from memory")
            self._session_token = None
            self._token_timestamp = None
            return None
        
        return self._session_token
    
    def get_token(self) -> str:
        """Get fresh Fyers access token through complete authentication flow"""
        headers = {
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        }
        
        s = requests.Session()
        s.headers.update(headers)
        
        try:
            logger.info("Starting authentication flow...")
            
            # Step 1: Send login OTP
            data1 = f'{{"fy_id":"{base64.b64encode(f"{self.username}".encode()).decode()}","app_id":"2"}}'
            r1 = s.post("https://api-t2.fyers.in/vagator/v2/send_login_otp_v2", data=data1)
            
            if r1.status_code != 200:
                raise Exception(f"Failed to send OTP: {r1.text}")
            
            request_key = r1.json()["request_key"]
            logger.info("OTP sent successfully")
            
            # Step 2: Verify OTP
            data2 = f'{{"request_key":"{request_key}","otp":{self.totp(self.totp_key)}}}'
            r2 = s.post("https://api-t2.fyers.in/vagator/v2/verify_otp", data=data2)
            
            if r2.status_code != 200:
                raise Exception(f"Failed to verify OTP: {r2.text}")
            
            request_key = r2.json()["request_key"]
            logger.info("OTP verified successfully")
            
            # Step 3: Verify PIN
            data3 = f'{{"request_key":"{request_key}","identity_type":"pin","identifier":"{base64.b64encode(f"{self.pin}".encode()).decode()}"}}'
            r3 = s.post("https://api-t2.fyers.in/vagator/v2/verify_pin_v2", data=data3)
            
            if r3.status_code != 200:
                raise Exception(f"Failed to verify PIN: {r3.json()}")
            
            logger.info("PIN verified successfully")
            
            # Step 4: Get authorization code
            headers = {
                "authorization": f"Bearer {r3.json()['data']['access_token']}", 
                "content-type": "application/json; charset=UTF-8"
            }
            data4 = f'{{"fyers_id":"{self.username}","app_id":"{self.client_id[:-4]}","redirect_uri":"{self.redirect_uri}","appType":"100","code_challenge":"","state":"abcdefg","scope":"","nonce":"","response_type":"code","create_cookie":true}}'
            r4 = s.post("https://api-t1.fyers.in/api/v3/token", headers=headers, data=data4)
            
            if r4.status_code != 308:
                raise Exception(f"Failed to get authorization code: {r4.json()}")
            
            parsed = urlparse(r4.json()["Url"])
            auth_code = parse_qs(parsed.query)["auth_code"][0]
            logger.info("Authorization code obtained")
            
            # Step 5: Generate final access token
            session = fyersModel.SessionModel(
                client_id=self.client_id, 
                secret_key=self.secret_key, 
                redirect_uri=self.redirect_uri, 
                response_type="code", 
                grant_type="authorization_code"
            )
            session.set_token(auth_code)
            response = session.generate_token()
            
            if response.get("s") != "ok":
                raise Exception(f"Failed to generate token: {response}")
            
            logger.info("Access token generated successfully")
            return response["access_token"]
            
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            raise
        finally:
            s.close()
    
    def init_token(self) -> str:
        """Initialize token with retry mechanism (3 attempts)"""
        attempts = 3
        for attempt in range(attempts):
            try:
                logger.info(f"Getting token, attempt {attempt + 1}/{attempts}")
                token = self.get_token()
                self.store_token_in_session(token)
                logger.info("Token successfully obtained and stored in session")
                return token
                
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt < attempts - 1:
                    logger.info("Retrying in 10 seconds...")
                    time.sleep(10)
                else:
                    logger.error("Max retry attempts reached. Could not retrieve token.")
                    raise
    
    def is_token_valid(self, token: str) -> bool:
        """Test if token is valid by making a profile API call"""
        try:
            fyers = self.create_fyers_client(token)
            profile = fyers.get_profile()
            return profile.get('s') == 'ok'
        except Exception as e:
            logger.warning(f"Token validation failed: {e}")
            return False
    
    def create_fyers_client(self, token: str) -> fyersModel.FyersModel:
        """Create Fyers client instance with proper error handling"""
        try:
            log_path = os.getenv('FYERS_LOG_PATH', "/tmp/")
            return fyersModel.FyersModel(client_id=self.client_id, token=token, is_async=False, log_path=log_path)
        except Exception as e:
            logger.error(f"Error creating Fyers client: {e}")
            raise
    
    def get_valid_token(self) -> str:
        """Get valid token, refresh if needed"""
        # Try to get existing session token first
        token = self.get_session_token()
        
        if token and self.is_token_valid(token):
            logger.info("Using existing valid session token")
            return token
        
        # Get new token if session token is invalid or expired
        logger.info("Getting new token (session token invalid/expired)")
        return self.init_token()

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with Fyers token management"""
    try:
        logger.info("Initializing Fyers MCP Server...")
        
        setup_fyers_logging()
        
        if not validate_environment():
            raise Exception("Environment validation failed")
        
        token_manager = FyersTokenManager()
        
        # Test connection
        token = token_manager.get_valid_token()
        fyers = token_manager.create_fyers_client(token)
        profile = fyers.get_profile()
        
        if profile.get('s') == 'ok':
            logger.info("✓ Connected to Fyers API successfully")
            logger.info(f"✓ User: {profile.get('data', {}).get('name', 'Unknown')}")
        else:
            raise Exception(f"Failed to connect to Fyers API: {profile}")
            
    except Exception as e:
        logger.error(f"Failed to initialize Fyers connection: {e}")
        raise
    
    try:
        yield AppContext(token_manager=token_manager)
    finally:
        logger.info("Shutting down Fyers MCP Server")

def get_fyers_client(ctx: Context) -> fyersModel.FyersModel:
    """Get authenticated Fyers client from context"""
    try:
        token_manager = ctx.request_context.lifespan_context.token_manager
        token = token_manager.get_valid_token()
        return token_manager.create_fyers_client(token)
    except Exception as e:
        logger.error(f"Error getting Fyers client: {e}")
        raise

# Create MCP server with lifespan management
mcptools = FastMCP(
    "Fyers Trading Server",
    dependencies=["fyers-apiv3", "pyotp", "requests"],
    lifespan=app_lifespan
)

# TOOLS - Trading Operations

@mcptools.tool()
async def get_historical_data(
    ctx: Context,
    symbol: str,
    range_from: str,
    range_to: str,
    resolution: str = "1D",
    cont_flag: int = 1
) -> str:
    """Get historical market data for a symbol"""
    try:
        fyers = get_fyers_client(ctx)
        data = {
            "symbol": symbol,
            "resolution": resolution,
            "date_format": "1",
            "range_from": range_from,
            "range_to": range_to,
            "cont_flag": cont_flag
        }
        response = fyers.history(data)
        return json.dumps(response, indent=2)
    except Exception as e:
        logger.error(f"Error getting historical data: {e}")
        return json.dumps({"error": str(e), "s": "error"}, indent=2)

@mcptools.tool()
async def place_order(
    ctx: Context,
    symbol: str,
    qty: int,
    type: int,
    side: int,
    productType: str,
    limitPrice: float = 0,
    stopPrice: float = 0,
    validity: str = "DAY",
    offlineOrder: str = "False",
    stopLoss: float = 0,
    takeProfit: float = 0
) -> str:
    """Place a trading order"""
    try:
        fyers = get_fyers_client(ctx)
        data = {
            "symbol": symbol,
            "qty": qty,
            "type": type,
            "side": side,
            "productType": productType,
            "limitPrice": limitPrice,
            "stopPrice": stopPrice,
            "validity": validity,
            "disclosedQty": 0,
            "offlineOrder": offlineOrder,
            "stopLoss": stopLoss,
            "takeProfit": takeProfit
        }
        response = fyers.place_order(data)
        return json.dumps(response, indent=2)
    except Exception as e:
        logger.error(f"Error placing order: {e}")
        return json.dumps({"error": str(e), "s": "error"}, indent=2)

@mcptools.tool()
async def modify_order(
    ctx: Context,
    id: str,
    type: Optional[int] = None,
    qty: Optional[int] = None,
    limitPrice: Optional[float] = None,
    stopPrice: Optional[float] = None
) -> str:
    """Modify an existing order"""
    try:
        fyers = get_fyers_client(ctx)
        data = {"id": id}
        if type is not None:
            data["type"] = type
        if qty is not None:
            data["qty"] = qty
        if limitPrice is not None:
            data["limitPrice"] = limitPrice
        if stopPrice is not None:
            data["stopPrice"] = stopPrice
        
        response = fyers.modify_order(data)
        return json.dumps(response, indent=2)
    except Exception as e:
        logger.error(f"Error modifying order: {e}")
        return json.dumps({"error": str(e), "s": "error"}, indent=2)

@mcptools.tool()
async def cancel_order(ctx: Context, id: str) -> str:
    """Cancel an existing order"""
    try:
        fyers = get_fyers_client(ctx)
        data = {"id": id}
        response = fyers.cancel_order(data)
        return json.dumps(response, indent=2)
    except Exception as e:
        logger.error(f"Error canceling order: {e}")
        return json.dumps({"error": str(e), "s": "error"}, indent=2)

@mcptools.tool()
async def get_quotes(ctx: Context, symbols: str) -> str:
    """Get real-time quotes for symbols"""
    try:
        fyers = get_fyers_client(ctx)
        data = {"symbols": symbols}
        response = fyers.quotes(data)
        return json.dumps(response, indent=2)
    except Exception as e:
        logger.error(f"Error getting quotes: {e}")
        return json.dumps({"error": str(e), "s": "error"}, indent=2)

@mcptools.tool()
async def get_market_depth(ctx: Context, symbol: str, ohlcv_flag: str = "1") -> str:
    """Get market depth for a symbol"""
    try:
        fyers = get_fyers_client(ctx)
        data = {
            "symbol": symbol,
            "ohlcv_flag": ohlcv_flag
        }
        response = fyers.depth(data)
        return json.dumps(response, indent=2)
    except Exception as e:
        logger.error(f"Error getting market depth: {e}")
        return json.dumps({"error": str(e), "s": "error"}, indent=2)

@mcptools.tool()
async def search_symbols(
    ctx: Context,
    symbol_query: str,
    instrument: str = "",
    exchange: str = ""
) -> str:
    """Search for trading symbols"""
    try:
        fyers = get_fyers_client(ctx)
        data = {
            "symbol_query": symbol_query,
            "instrument": instrument,
            "exchange": exchange
        }
        response = fyers.search_symbols(data)
        return json.dumps(response, indent=2)
    except Exception as e:
        logger.error(f"Error searching symbols: {e}")
        return json.dumps({"error": str(e), "s": "error"}, indent=2)

@mcptools.tool()
async def refresh_token(ctx: Context) -> str:
    """Refresh authentication token"""
    try:
        token_manager = ctx.request_context.lifespan_context.token_manager
        # Force token refresh by clearing session
        token_manager._session_token = None
        token_manager._token_timestamp = None
        token = token_manager.get_valid_token()
        return json.dumps({
            "message": "Token refreshed successfully",
            "token_preview": f"{token[:20]}...",
            "timestamp": datetime.now().isoformat(),
            "s": "ok"
        }, indent=2)
    except Exception as e:
        logger.error(f"Error refreshing token: {e}")
        return json.dumps({"error": str(e), "s": "error"}, indent=2)

# TOOLS - Account Information (Converted from Resources)

@mcptools.tool()
async def get_profile(ctx: Context) -> str:
    """Get user profile information"""
    try:
        fyers = get_fyers_client(ctx)
        response = fyers.get_profile()
        return json.dumps(response, indent=2)
    except Exception as e:
        logger.error(f"Error getting profile: {e}")
        return json.dumps({"error": str(e), "s": "error"}, indent=2)

@mcptools.tool()
async def get_funds(ctx: Context) -> str:
    """Get account fund details"""
    try:
        fyers = get_fyers_client(ctx)
        response = fyers.funds()
        return json.dumps(response, indent=2)
    except Exception as e:
        logger.error(f"Error getting funds: {e}")
        return json.dumps({"error": str(e), "s": "error"}, indent=2)

@mcptools.tool()
async def get_positions(ctx: Context) -> str:
    """Get current positions"""
    try:
        fyers = get_fyers_client(ctx)
        response = fyers.positions()
        return json.dumps(response, indent=2)
    except Exception as e:
        logger.error(f"Error getting positions: {e}")
        return json.dumps({"error": str(e), "s": "error"}, indent=2)

@mcptools.tool()
async def get_holdings(ctx: Context) -> str:
    """Get current holdings"""
    try:
        fyers = get_fyers_client(ctx)
        response = fyers.holdings()
        return json.dumps(response, indent=2)
    except Exception as e:
        logger.error(f"Error getting holdings: {e}")
        return json.dumps({"error": str(e), "s": "error"}, indent=2)

@mcptools.tool()
async def get_orders(ctx: Context) -> str:
    """Get order book"""
    try:
        fyers = get_fyers_client(ctx)
        response = fyers.orderbook()
        return json.dumps(response, indent=2)
    except Exception as e:
        logger.error(f"Error getting orders: {e}")
        return json.dumps({"error": str(e), "s": "error"}, indent=2)

@mcptools.tool()
async def get_server_status(ctx: Context) -> str:
    """Get server status and configuration"""
    try:
        token_manager = ctx.request_context.lifespan_context.token_manager
        
        token_info = {
            "session_token_exists": token_manager._session_token is not None,
            "token_timestamp": token_manager._token_timestamp.isoformat() if token_manager._token_timestamp else None,
            "token_age_hours": None
        }
        
        if token_manager._token_timestamp:
            elapsed = datetime.now() - token_manager._token_timestamp
            token_info["token_age_hours"] = round(elapsed.total_seconds() / 3600, 2)
        
        status = {
            "server": "Fyers MCP Server",
            "status": "Connected",
            "storage_type": "Session-based (in-memory)",
            "token_info": token_info,
            "client_id_preview": f"{token_manager.client_id[:10]}...",
            "redirect_uri": token_manager.redirect_uri,
            "tools": 14,
            "s": "ok"
        }
        return json.dumps(status, indent=2)
    except Exception as e:
        logger.error(f"Error getting server status: {e}")
        return json.dumps({"error": str(e), "s": "error"}, indent=2)

def main():
    """Main entry point - Initialize and start the MCP server"""
    try:
        print("🚀 Starting Fyers MCP Server...", file=sys.stderr)
        
        setup_fyers_logging()
        
        if not validate_environment():
            print("❌ Environment validation failed. Exiting.", file=sys.stderr)
            sys.exit(1)
        
        print("✅ Environment validation passed", file=sys.stderr)
        print("🔌 Starting MCP server...", file=sys.stderr)
        
        mcptools.run()
        
    except Exception as e:
        print(f"❌ Fatal error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()