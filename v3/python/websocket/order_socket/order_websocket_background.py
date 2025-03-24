from fyers_apiv3.FyersWebsocket import order_ws

# Replace the sample access token with your actual access token obtained from Fyers
access_token = "XCXXXXXXM-100:eyJ0tHfZNSBoLo"

# Create a FyersDataSocket instance with the provided parameters
fyers = order_ws.FyersOrderSocket(
    access_token=access_token,  # Your access token for authenticating with the Fyers API.
    write_to_file=True,        # A boolean flag indicating whether to write data to a log file or not.
    log_path="",                # The path to the log file if write_to_file is set to True (empty string means current directory).
)

# Establish a connection to the Fyers WebSocket
fyers.connect()

# Specify the data type and symbols you want to subscribe to
# data_type = "OnOrders"
# data_type = "OnTrades"
# data_type = "OnPositions"
# data_type = "OnGeneral"
data_type = "OnOrders,OnTrades,OnPositions,OnGeneral"

fyers.subscribe(data_type=data_type)

# Keep the socket running to receive real-time data
fyers.keep_running()
