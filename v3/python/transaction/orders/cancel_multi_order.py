from fyers_apiv3 import fyersModel

client_id = "XC4XXXXM-100"
access_token = "eyJ0eXXXXXXXX2c5-Y3RgS8wR14g"

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,is_async=True, log_path="")


data =  [{
    "id": '808058117761'
},
{
    "id": '808058117762'
}]

response = fyers.cancel_basket_orders(data=data)
print(response)