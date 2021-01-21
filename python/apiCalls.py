moduleName = "apiCalls"
"""
    1.We need to first install fyers-apiv2(can be installed as 'pip install fyers-apiv2) if not installed.
    2.We then need to import fyersModel module from fyers_api directory(as done below).
"""
from fyers_api import fyersModel


def api_call(access_token, appId, log_path):
    functionName = "api_call"
    """
        :param access_token: "https://XXXXXX.com"
        :param app_id: "XXXXXXXXXXX"
        :param log_path: "home/gfxcgv/vgghvb/xxxx"
    """

    # If you want to make asynchronous API calls then assign the below variable as True and then pass it in the functions, by default its value is False
    is_async = False

    # Creating an instance of fyers model in order to call the apis
    fyers = fyersModel.FyersModel(token=access_token, is_async=is_async, log_path=log_path, client_id=appId)

    # Setting the AccessToken
    fyers.token = access_token

    ## uncomment the any of the following requests to send a particular request and get the required data

    # print(fyers.get_profile())
    # print(fyers.tradebook())
    # print(fyers.positions())
    # print(fyers.holdings())
    # print(fyers.convert_position({"symbol":"MCX:SILVERMIC20AUGFUT","positionSide":"1","convertQty":"1","convertFrom":"MARGIN","convertTo":"INTRADAY"}))
    # print(fyers.funds())
    # print(fyers.orderbook())
    # print(fyers.cancel_order({'id':'8080582117761'}))
    # print(fyers.place_order({"symbol":"MCX:SILVERMIC20AUGFUT","qty":"1","type":"1","side":"1","productType":"INTRADAY","limitPrice":"76700","stopPrice":"0","disclosedQty":"0","validity":"DAY","offlineOrder":"False","stopLoss":"0","takeProfit":"0"}))
    # print(fyers.modify_order({"id":"808058117761", "qty":"0","type":"1","limitPrice":"71100","stopPrice":"0"})) #modify instead of update
    # print(fyers.minquantity())
    # print(fyers.get_orders({'id':'808078094451'}))
    # print(fyers.market_status())
    # print(fyers.exit_positions({"id":"MCX:SILVERMIC20AUGFUT-MARGIN"}))
    # print(fyers.generate_data_token({"vendorApp":"0KMS0EZVXI"}))
    # print(fyers.cancel_basket_orders([{"id":"120080780536"},{"id":"120080777069"}]))
    # print(fyers.place_basket_orders([{"symbol":"NSE:SBIN-EQ","qty":"1","type":"1","side":"1","productType":"INTRADAY","limitPrice":"191","stopPrice":"0","disclosedQty":"0","validity":"DAY","offlineOrder":"False","stopLoss":"0","takeProfit":"0"},{"symbol":"NSE:SBIN-EQ","qty":"1","type":"1","side":"1","productType":"INTRADAY","limitPrice":"191","stopPrice":"0","disclosedQty":"0","validity":"DAY","offlineOrder":"False","stopLoss":"0","takeProfit":"0"}]))
    # print(fyers.modify_basket_orders([{"id":"120080780536", "type":1, "limitPrice": 190, "stopPrice":0},{"id":"120080777069", "type":1, "limitPrice": 190}]))

if __name__ == '__main__':
    # the access token returned fro generate_access_token(x,x,x,x) function from getAccessToken.py module
    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2MTExNTI5MzUsImV4cCI6MTYxMTE4OTA1NSwibmJmIjoxNjExMTUyOTM1LCJhdWQiOlsieDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCZ0NENG51WjBNblNIam1ibHhzZDBZZUd4aW1jR09UTUo3c3R4MVZZTi1WekdkVUdrU1g0U09vWHFqMFBkMW8yZVZTanlHYWhMM21CT3lIb2g3WS1JdTRyX0NlV2NxN2hna1dzQ09iVHROT3A4TmtLST0iLCJkaXNwbGF5X25hbWUiOiJBUktBIE1BTkRXXXXXXXXXXXXXXXXXXXXXXXIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJZIn0.51x5O0gpHC7xNpGukWPQZU7wDZY2B_XNxB8Hlulspro"

    # The app id we get after creating the app
    appId = "EXXXXXXVWZ"

    # The system path where we want to store the logs e.g-c:\user\vvvv\xxxx\nnnn
    log_path = r"/home/fyers/Desktop/fyers-api-py/fyers_api"

    ## uncomment any of the function in the api_call to get the required output
    api_call(access_token, appId, log_path)
