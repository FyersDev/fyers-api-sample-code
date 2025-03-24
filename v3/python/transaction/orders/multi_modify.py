from fyers_apiv3 import fyersModel

client_id = "XC4XXXXM-100"
access_token = "eyJ0eXXXXXXXX2c5-Y3RgS8wR14g"
# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,is_async=False, log_path="")


data = [{
  "id": "8102710298291",
  "type": 1,
  "limitPrice": 61049,
  "qty": 1
},
{
  "id": "8102710298292",
  "type": 1,
  "limitPrice": 61049,
  "qty": 1
}]

response = fyers.modify_basket_orders(data=data)
print(response)