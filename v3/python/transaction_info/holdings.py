from fyers_apiv3 import fyersModel

client_id = "XC4XXXXM-100"
access_token = "eyJ0eXXXXXXXX2c5-Y3RgS8wR14g"

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,is_async=True, log_path="")

response = fyers.holdings()
print(response)


{
   "code":200,
   "message":"",
   "s":"ok",
   "overall":{
      "count_total":1,
      "pnl_perc":21.9136,
      "total_current_value":23.700000000000003,
      "total_investment":19.44,
      "total_pl":4.26
   },
   "holdings":[
      {
         "costPrice":6.48,
         "id":0,
         "fyToken":"101000000014366",
         "symbol":"NSE:IDEA-EQ",
         "isin":"INE669E01016",
         "quantity":3,
         "exchange":10,
         "segment":10,
         "qty_t1":0,
         "remainingQuantity":3,
         "collateralQuantity":0,
         "remainingPledgeQuantity":3,
         "pl":4.26,
         "ltp":7.9,
         "marketVal":23.700000000000003,
         "holdingType":"HLD"
      }
   ]
}