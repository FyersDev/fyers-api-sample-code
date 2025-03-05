from fyers_apiv3.FyersWebsocket.tbt_ws import FyersTbtSocket, SubscriptionModes

# Replace the sample access token with your actual access token obtained from Fyers
access_token = "XCXXXXXXM-100:eyJ0tHfZNSBoLo"

# Create a FyersDataSocket instance with the provided parameters
fyers = FyersTbtSocket(
    access_token=access_token,  # Your access token for authenticating with the Fyers API.
    write_to_file=True,        # A boolean flag indicating whether to write data to a log file or not.
    log_path="",                # The path to the log file if write_to_file is set to True (empty string means current directory).
)


# Establish a connection to the Fyers WebSocket
fyers.connect()

mode = SubscriptionModes.DEPTH
Channel = '1'
# Subscribe to the specified symbols and data type
symbols = ['NSE:NIFTY25MARFUT']

fyers.subscribe(symbol_tickers=symbols, channelNo=Channel, mode=mode)
fyers.switchChannel(resume_channels=[Channel], pause_channels=[])

# Keep the socket running to receive real-time data
fyers.keep_running()
