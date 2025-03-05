from  fyers_apiv3.FyersWebsocket.tbt_ws import FyersTbtSocket, SubscriptionModes

def on_depth_update(ticker, message):
    """
    Callback function to handle incoming messages from the FyersDataSocket WebSocket.

    Parameters:
        ticker (str): The symbol for which the message is received.
        message (dict): The received message from the WebSocket.

    """
    print("Depth Response:", ticker, message)


def onerror_message( message):
    """
    Callback function to handle incoming messages from the FyersDataSocket WebSocket.

    Parameters:
        message (str): error message from the server

    """
    print("server returned error:", message)


def onerror(message):
    """
    Callback function to handle WebSocket errors.

    Parameters:
        message (dict): The error message received from the WebSocket.


    """
    print("Error:", message)


def onclose(message):
    """
    Callback function to handle WebSocket connection close events.
    """
    print("Connection closed:", message)


def onopen():
    """
    Callback function to subscribe to data type and symbols upon WebSocket connection.

    """
    print("Connection opened")
    # Specify the data type and symbols you want to subscribe to
    mode = SubscriptionModes.DEPTH
    Channel = '1'
    # Subscribe to the specified symbols and data type
    symbols = ['NSE:NIFTY25MARFUT']
    
    fyers.subscribe(symbol_tickers=symbols, channelNo=Channel, mode=mode)
    fyers.switchChannel(resume_channels=[Channel], pause_channels=[])

    # Keep the socket running to receive real-time data
    fyers.keep_running()


# Replace the sample access token with your actual access token obtained from Fyers
access_token = "GT2V66D5Y4-101:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE3NDExNTI1MzgsImV4cCI6MTc0MTIyMTA1OCwibmJmIjoxNzQxMTUyNTM4LCJhdWQiOlsieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbngtRWE4U255bGM3Z1dfMFJtc19QMlVtSTdrZFQzS3ZsNTBTQVAtQURKcnpfR0t4ajJvTzVveW52VHVydHNSRXdTUmMtTDN0NTVWaW51cEJJZnBDU0NFTHZBNlZhYVRaV0tNY1pnUXVUM0lJTS01Yz0iLCJkaXNwbGF5X25hbWUiOiJQQVRJTCBQSVlVU0ggU1VSRVNIIiwib21zIjoiSzEiLCJoc21fa2V5IjoiYTM1MmYxN2I5MmRiZTU4NTgyMzg2MmRkYjMxZWE1NTY1OGE0MTc2OTM4MmM3NDNlYTQyMjg1OGYiLCJpc0RkcGlFbmFibGVkIjoiTiIsImlzTXRmRW5hYmxlZCI6Ik4iLCJmeV9pZCI6IlhQMDE0NzAiLCJhcHBUeXBlIjoxMDEsInBvYV9mbGFnIjoiTiJ9.AJA0-4FIWnlviV6vpIHCxmQbfbq2YhoYAsrCYvbEu-o"

fyers = FyersTbtSocket(
    access_token=access_token,  # Your access token for authenticating with the Fyers API.
    write_to_file=False,        # A boolean flag indicating whether to write data to a log file or not.
    log_path="",                # The path to the log file if write_to_file is set to True (empty string means current directory).
    on_open=onopen,          # Callback function to be executed upon successful WebSocket connection.
    on_close=onclose,           # Callback function to be executed when the WebSocket connection is closed.
    on_error=onerror,           # Callback function to handle any WebSocket errors that may occur.
    on_depth_update=on_depth_update, # Callback function to handle depth-related events from the WebSocket
    on_error_message=onerror_message         # Callback function to handle server-related erros from the WebSocket.
)


# Establish a connection to the Fyers WebSocket
fyers.connect()

