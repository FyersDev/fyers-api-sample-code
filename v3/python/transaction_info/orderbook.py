from fyers_apiv3 import fyersModel

client_id = "XC4XXXXM-100"
access_token = "eyJ0eXXXXXXXX2c5-Y3RgS8wR14g"

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,is_async=False, log_path="")

response = fyers.orderbook()
print(response)



{
   "code":200,
   "message":"",
   "s":"ok",
   "orderBook": [{
            "clientId":"XXXXX86",
            "exchange":10,
            "fyToken":"101000000014366",
            "id":"23080444447604",
            "offlineOrder":false,
            "source":"W",
            "status":2,
            "type":2,
            "pan":"",
            "limitPrice":8.1,
            "productType":"INTRADAY",
            "qty":1,
            "disclosedQty":0,
            "remainingQuantity":0,
            "segment":10,
            "symbol":"NSE:IDEA-EQ",
            "description":"VODAFONE IDEA LIMITED",
            "ex_sym":"IDEA",
            "orderDateTime":"02-Aug-2023 13:01:42",
            "side":1,
            "orderValidity":"DAY",
            "stopPrice":0,
            "tradedPrice":8.1,
            "filledQty":1,
            "exchOrdId":"1100000024706527",
            "message":"",
            "ch":-0.35,
            "chp":-4.24,
            "lp":7.9,
            "orderNumStatus":"23080444447604:2",
            "slNo":1
        }]
}
