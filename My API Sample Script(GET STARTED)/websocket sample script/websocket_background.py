
from fyers_api.Websocket import ws
from fyers_api import fyersModel

fyers = fyersModel.FyersModel(token="access_token as defined in main block",is_async=False,client_id="client_id(APP_ID)") ## Create a fyersModel object if in any scenario you want to call the trading and data apis when certain condiiton in websocket data is met so that can be triggered by calling the method/object after subscribing and before the keep_running method as shown in run_process_background_symbol_data


def run_process_background_symbol_data(access_token):
    '''This function is used for running the symbol_Data in background 
    1. log_path here is configurable this specifies where the output will be stored for you if the process is running in background
    2. data_type == SymbolData this specfies while using this function you will be able to connect to symbolwebsocket to get the symbolData
    3. run_background = True specifies that the process will be running in background and the data will be stored in the log file the path to which is specified over the log_path'''

    data_type = "symbolData"
    symbol =["NSE:NIFTY50-INDEX","NSE:NIFTYBANK-INDEX","NSE:SBIN-EQ","NSE:HDFC-EQ","NSE:IOC-EQ"]
    fs = ws.FyersSocket(access_token=access_token,run_background=True,log_path="/home/Downloads/")
    fs.websocket_data = custom_message
    fs.subscribe(symbol=symbol,data_type=data_type)
    
    print(fyers.get_profile())
    print(fyers.orderbook())
    fs.keep_running()


def run_process_background_order_update(access_token):   
    '''This function is used for running the order_update in background 
    1. log_path here is configurable this specifies where the output will be stored for you if the process is running in background
    2. data_type == orderUpdate this specfies while using this function you will be able to connect to orderwebsocket to get the orderUpdate
    3. run_background = True specifies that the process will be running in background and the data will be stored in the log file the path to which is specified over the log_path'''

    data_type = "orderUpdate"
    fs = ws.FyersSocket(access_token=access_token,run_background=True,log_path="/home/Downloads/")
    fs.websocket_data = custom_message
    fs.subscribe(data_type=data_type)
    fs.keep_running()


def custom_message(msg):       ### This function can be anything which you want to configure at your end 
    print (f"Custom:{msg}") 


def main():
    access_token = "eyJ0eXDRzdW5tQ3FmQWN6bDVESkZsMEJLeEw3N3E5RUttMWRYNzcta05VaXhiNE4xY3ZoVGU0RGx4YUFBTERuekhqeU4xQT0iLCJkaXNwbGF5X25hbWUiOiJQSVlVU0ggUkFKRU5EU**************************kEgS0FQU0UiLCJmeV9pZCI6IkRQMDA0MDQiLCJhcHBUeXBlIjoxMDAsInBvYV9mbGFnIjoiTiJ9.SqubA2d3axSDQW3xah8d_ZI_xFQSkDeSExv4EvotuGs"
    ## For regular api calls you the access_token as mentioned above 
    ### Insert the accessToken and app_id over here in the following format for subscribing the websocket data (APP_ID:access_token) 
    access_token_websocket= "L9*****6BW-100:eyJ0eXDRzdW5tQ3FmQWN6bDVESkZsMEJLeEw3N3E5RUttMWRYNzcta05VaXhiNE4xY3ZoVGU0RGx4YUFBTERuekhqeU4xQT0iLCJkaXNwbGF5X25hbWUiOiJQSVlVU0ggUkFKRU5EUkEgS0FQU0UiLCJmeV9pZCI6IkRQMDA0MDQiLCJhcHBUeXBlIjoxMDAsInBvYV9mbGFnIjoiTiJ9.SqubA2d3axSDQW3xah8d_ZI_xFQSkDeSExv4EvotuGs"

    ## run a specific process you need to connect to get the updates on 
    run_process_background_symbol_data(access_token_websocket)

    run_process_background_order_update(access_token_websocket)
    
if __name__ == '__main__':
	main()