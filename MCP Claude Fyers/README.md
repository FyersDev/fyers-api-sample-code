# Fyers MCP Server

A Model Context Protocol (MCP) server for integrating Fyers API with Claude Desktop, providing comprehensive trading functionality including authentication, market data, order management, and account information.

## Features

- 🔐 **Secure Authentication** - Automated token management with TOTP-based 2FA
- 📊 **Market Data** - Real-time quotes, historical data, and market depth
- 📈 **Trading Operations** - Place, modify, and cancel orders
- 💼 **Account Management** - Profile, funds, positions, and holdings
- 🔍 **Symbol Search** - Find trading instruments across exchanges
- ♻️ **Auto Token Refresh** - Intelligent token management with retry mechanisms

## Tools Available

### Trading Operations
- `get_historical_data` - Fetch historical market data
- `place_order` - Place trading orders
- `modify_order` - Modify existing orders
- `cancel_order` - Cancel orders
- `get_quotes` - Real-time price quotes
- `get_market_depth` - Market depth information
- `search_symbols` - Search for trading symbols

### Account Information
- `get_profile` - User profile details
- `get_funds` - Account fund information
- `get_positions` - Current trading positions
- `get_holdings` - Investment holdings
- `get_orders` - Order book
- `get_server_status` - Server status and configuration
- `refresh_token` - Manual token refresh

## Prerequisites

### Python Dependencies
```bash
pip install fyers-apiv3 mcp pyotp requests
```

### Fyers API Credentials
You'll need to obtain the following from your Fyers account:
- **App Client ID** - From Fyers API dashboard
- **App Secret Key** - From Fyers API dashboard
- **Username** - Your Fyers login ID
- **TOTP Key** - For 2FA authentication
- **PIN** - Your trading PIN

## Installation & Setup

### Step 1: Download the Server
Save the `mcp_fyers_server.py` file to your desired location.

### Step 2: Install Dependencies
```bash
pip install fyers-apiv3 mcp pyotp requests
```

### Step 3: Configure Claude Desktop

#### For macOS
Edit your Claude Desktop configuration file:
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

#### For Windows
Edit your Claude Desktop configuration file:
```bash
%APPDATA%/Claude/claude_desktop_config.json
```

Add the following configuration (replace with your actual paths and credentials):

```json
{
  "mcpServers": {
    "fyers-mcp-server": {
      "command": "/opt/homebrew/bin/python3.10",
      "args": ["/Users/yourusername/path/to/mcp_fyers_server.py"],
      "env": {
        "APP_CLIENT_ID": "your-client-id-100",
        "APP_SECRET_KEY": "your-secret-key",
        "APP_REDIRECT_URI": "https://www.google.com",
        "FYERS_USERNAME": "your-fyers-username",
        "FYERS_TOTP_KEY": "your-totp-secret-key",
        "FYERS_PIN": "your-trading-pin"
      }
    }
  }
}
```

### Step 4: Find Your Python Path
```bash
# On macOS/Linux
which python3

# On Windows
where python
```

### Step 5: Restart Claude Desktop
Close and reopen Claude Desktop application.

## Configuration Details

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `APP_CLIENT_ID` | Your Fyers App Client ID | `ABC123-100` |
| `APP_SECRET_KEY` | Your Fyers App Secret Key | `XYZ789SECRET` |
| `APP_REDIRECT_URI` | Redirect URI (can be any valid URL) | `https://www.google.com` |
| `FYERS_USERNAME` | Your Fyers login username | `YourUsername` |
| `FYERS_TOTP_KEY` | TOTP secret key for 2FA | `ABCD1234EFGH5678` |
| `FYERS_PIN` | Your 4-digit trading PIN | `1234` |

### Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FYERS_LOG_PATH` | Path for Fyers API logs | Disabled (`/dev/null`) |

## Usage Examples

Once configured, you can interact with the Fyers API through Claude:

### Get Market Data
```
"Get historical data for RELIANCE from 2024-01-01 to 2024-01-31"
```

### Check Account Status
```
"Show my current positions and account funds"
```

### Place Orders
```
"Place a buy order for 10 shares of TCS at market price"
```

### Search Symbols
```
"Search for symbols related to 'HDFC'"
```

## Security Features

- **Session-based Token Storage** - Tokens stored in memory only, not persisted to disk
- **Automatic Token Refresh** - Intelligent token management with validation
- **TOTP Authentication** - Secure 2FA using time-based one-time passwords
- **Environment Variable Protection** - Sensitive data stored in configuration only

## Troubleshooting

### Common Issues

1. **"Missing required environment variables"**
   - Ensure all required variables are set in your configuration
   - Check for typos in variable names

2. **"Authentication failed"**
   - Verify your TOTP key is correct
   - Ensure your PIN and credentials are accurate
   - Check if your Fyers account has API access enabled

3. **"Token expired"**
   - Use the `refresh_token` tool to get a new token
   - The server automatically refreshes tokens as needed

4. **"Python not found"**
   - Update the `command` path in your configuration
   - Use the full path to your Python executable

### Debug Mode
Set `FYERS_LOG_PATH` to a file path to enable detailed logging:
```json
"FYERS_LOG_PATH": "/tmp/fyers.log"
```

## API Reference

For detailed information about Fyers API parameters and responses, refer to:
- [Fyers API Documentation](https://myapi.fyers.in/docs/)
- [Fyers API v3 Python SDK](https://github.com/fyers-api/fyers-api-sdk)

## Support

For issues related to:
- **Fyers API**: Contact Fyers support or check their documentation
- **MCP Integration**: Check the configuration and ensure all dependencies are installed
- **Claude Desktop**: Refer to Anthropic's documentation

## License

This project is provided as-is for educational and personal use. Please ensure compliance with Fyers API terms of service and applicable regulations.

---

**⚠️ Important**: This tool provides access to live trading functions. Always test with small amounts and understand the risks involved in automated trading.