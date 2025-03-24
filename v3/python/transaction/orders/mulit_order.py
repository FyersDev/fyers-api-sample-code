from fyers_apiv3 import fyersModel

client_id = "XC4XXXXM-100"
access_token = "eyJ0eXXXXXXXX2c5-Y3RgS8wR14g"
# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,is_async=False, log_path="")

data = [{
    "symbol":"NSE:SBIN-EQ",
    "qty":1,
    "type":2,
    "side":1,
    "productType":"INTRADAY",
    "limitPrice":0,
    "stopPrice":0,
    "validity":"DAY",
    "disclosedQty":0,
    "offlineOrder":False,
},
{
    "symbol":"NSE:IDEA-EQ",
    "qty":1,
    "type":2,
    "side":1,
    "productType":"INTRADAY",
    "limitPrice":0,
    "stopPrice":0,
    "validity":"DAY",
    "disclosedQty":0,
    "offlineOrder":False,
},{
    "symbol":"NSE:SBIN-EQ",
    "qty":1,
    "type":2,
    "side":1,
    "productType":"INTRADAY",
    "limitPrice":0,
    "stopPrice":0,
    "validity":"DAY",
    "disclosedQty":0,
    "offlineOrder":False,
},
{
    "symbol":"NSE:IDEA-EQ",
    "qty":1,
    "type":2,
    "side":1,
    "productType":"INTRADAY",
    "limitPrice":0,
    "stopPrice":0,
    "validity":"DAY",
    "disclosedQty":0,
    "offlineOrder":False,
}]

response = fyers.place_basket_orders(data=data)
print(response)