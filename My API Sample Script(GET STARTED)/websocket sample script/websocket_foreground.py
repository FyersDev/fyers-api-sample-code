
from fyers_api.Websocket import ws


def run_process_foreground_symbol_data(access_token):
    '''This function is used for running the symbolData in foreground 
    1. log_path here is configurable this specifies where the output will be stored for you
    2. data_type == symbolData this specfies while using this function you will be able to connect to symbolwebsocket to get the symbolData
    3. run_background = False specifies that the process will be running in foreground'''
    data_type = "symbolData"
    # symbol = ["NSE:SBIN-EQ","NSE:ONGC-EQ"]   ##NSE,BSE sample symbols
    symbol =["NSE:NIFTY50-INDEX","NSE:NIFTYBANK-INDEX","NSE:SBIN-EQ","NSE:HDFC-EQ","NSE:IOC-EQ"]
    # symbol =["MCX:SILVERMIC21NOVFUT","MCX:GOLDPETAL21SEPTFUT"]
    fs = ws.FyersSocket(access_token=access_token,run_background=False,log_path="/home/Downloads/")
    fs.websocket_data = custom_message
    fs.subscribe(symbol=symbol,data_type=data_type)
    fs.keep_running()


def run_process_foreground_order_update(access_token):
    '''This function is used for running the order_update in background 
    1. log_path here is configurable this specifies where the output will be stored for you.
    2. data_type == orderUpdate this specfies while using this function you will be able to connect to orderwebsocket to get the orderUpdate
    3. run_background = False specifies that the process will be running in foreground '''
    data_type = "orderUpdate"
    fs = ws.FyersSocket(access_token=access_token,run_background=False,log_path="/home/Downloads/")
    fs.websocket_data = custom_message
    fs.subscribe(data_type=data_type)
    fs.keep_running()


def custom_message(msg):
    print (f"Custom:{msg}") 


def main():
    ### Insert the accessToken and app_id over here in the following format (APP_ID:access_token) 
    access_token= "L9****6BW-100:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2MzM2Njc5MjksImV4cCI6MTYzMzczOTQ0OSwibmJmIjoxNjMzNjY3OTI5LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDow**********************************aFg4dFotcFZpOGdvYmMtMlRfNmNmYlowQlVFbVJFel9XSjJCRmJTRURWUm1GbDRzdW5tQ3FmQWN6bDVESkZsMEJLeEw3N3E5RUttMWRYNzcta05VaXhiNE4xY3ZoVGU0RGx4YUFBTERuekhqeU4xQT0iLCJkaXNwbGF5X25hQMDA0MDQiLCJhcHBUeXBlIjoxMDAsInBvYV9mbGFnIjoiTiJ9.SqubA2d3axSDQW3xah8d_ZI_xFQSkDeSExv4EvotuGs"

    ## run a specific process you need to connect to get the updates on
    run_process_foreground_symbol_data(access_token)

    # run_process_foreground_order_update(access_token)
    
if __name__ == '__main__':
	main()