from fyers_apiv3 import fyersModel

client_id = "XC4XXXXM-100"
access_token = "eyJ0eXXXXXXXX2c5-Y3RgS8wR14g"

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,is_async=True, log_path="")

# Make a request to get the funds information
response = fyers.funds()
print(response)



{
   "code":200,
   "message":"",
   "s":"ok",
   "fund_limit":[
      {
         "id":1,
         "title":"Total Balance",
         "equityAmount":58.150000000000006,
         "commodityAmount":0
      },
      {
         "id":2,
         "title":"Utilized Amount",
         "equityAmount":0.3,
         "commodityAmount":0
      },
      {
         "id":3,
         "title":"Clear Balance",
         "equityAmount":58.150000000000006,
         "commodityAmount":0
      },
      {
         "id":4,
         "title":"Realized Profit and Loss",
         "equityAmount":-0.3,
         "commodityAmount":0
      },
      {
         "id":5,
         "title":"Collaterals",
         "equityAmount":0,
         "commodityAmount":0
      },
      {
         "id":6,
         "title":"Fund Transfer",
         "equityAmount":0,
         "commodityAmount":0
      },
      {
         "id":7,
         "title":"Receivables",
         "equityAmount":0,
         "commodityAmount":0
      },
      {
         "id":8,
         "title":"Adhoc Limit",
         "equityAmount":0,
         "commodityAmount":0
      },
      {
         "id":9,
         "title":"Limit at start of the day",
         "equityAmount":58.45,
         "commodityAmount":0
      },
      {
         "id":10,
         "title":"Available Balance",
         "equityAmount":58.150000000000006,
         "commodityAmount":0
      }
   ]
}