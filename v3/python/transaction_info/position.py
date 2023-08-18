from fyers_apiv3 import fyersModel

client_id = "XC4XXXXM-100"
access_token = "eyJ0eXXXXXXXX2c5-Y3RgS8wR14g"

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,is_async=False, log_path="")

response = fyers.positions()
print(response)


















{
   "code":200,
   "message":"",
   "s":"ok",
   "netPositions":[
      {
         "symbol":"NSE:IDEA-EQ",
         "id":"NSE:IDEA-EQ-INTRADAY",
         "buyAvg":8.1,
         "buyQty":3,
         "buyVal":24.3,
         "sellAvg":8,
         "sellQty":3,
         "sellVal":24,
         "netAvg":0,
         "netQty":0,
         "side":0,
         "qty":0,
         "productType":"INTRADAY",
         "realized_profit":-0.29999999999999893,
         "crossCurrency":"",
         "rbiRefRate":1,
         "fyToken":"101000000014366",
         "exchange":10,
         "segment":10,
         "dayBuyQty":3,
         "daySellQty":3,
         "cfBuyQty":0,
         "cfSellQty":0,
         "qtyMulti_com":1,
         "pl":-0.29999999999999893,
         "unrealized_profit":0,
         "ltp":7.9,
         "slNo":0
      }
   ],
   "overall":{
      "count_open":0,
      "count_total":1,
      "pl_realized":-0.29999999999999893,
      "pl_total":-0.29999999999999893,
      "pl_unrealized":0
   }
}