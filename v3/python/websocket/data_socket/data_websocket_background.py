from fyers_apiv3.FyersWebsocket import data_ws


# Replace the sample access token with your actual access token obtained from Fyers
access_token = "XCXXXXXXM-100:eyJ0tHfZNSBoLo"

# Create a FyersDataSocket instance with the provided parameters
fyers = data_ws.FyersDataSocket(
    access_token=access_token,       # Access token in the format "appid:accesstoken"
    log_path="",                     # Path to save logs. Leave empty to auto-create logs in the current directory.
    litemode=False,                  # Lite mode disabled. Set to True if you want a lite response.
    write_to_file=True,              # Save response in a log file instead of printing it.
    reconnect=True,                  # Enable auto-reconnection to WebSocket on disconnection.
)

# Establish a connection to the Fyers WebSocket
fyers.connect()

# Specify the data type and symbols you want to subscribe to
data_type = "SymbolUpdate"
# data_type = "DepthUpdate"

# Subscribe to the specified symbols and data type
symbols = ['NSE:SBIN-EQ', 'NSE:ADANIENT-EQ']
fyers.subscribe(symbols=symbols, data_type=data_type)

# Keep the socket running to receive real-time data
fyers.keep_running()
