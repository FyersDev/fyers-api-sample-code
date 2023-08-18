from fyers_apiv3 import fyersModel

client_id = "XC4XXXXM-100"
access_token = "eyJ0eXXXXXXXX2c5-Y3RgS8wR14g"

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,is_async=False, log_path="")

response = fyers.tradebook()
print(response)



{
   "code":200,
   "message":"",
   "s":"ok",
   "tradeBook":[
      {
         "clientId":"XXXXX86",
         "exchange":10,
         "fyToken":"101000000014366",
         "orderNumber":"23080200259588",
         "exchangeOrderNo":"1100000024874314",
         "tradeNumber":"23080200259588-24758269",
         "tradePrice":8.05,
         "segment":10,
         "productType":"INTRADAY",
         "tradedQty":1,
         "symbol":"NSE:IDEA-EQ",
         "row":1690961636,
         "orderDateTime":"02-Aug-2023 13:03:56",
         "tradeValue":8.05,
         "side":-1,
         "orderType":2
      }
   ]
}