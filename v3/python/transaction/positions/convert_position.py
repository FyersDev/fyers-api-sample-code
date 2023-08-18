from fyers_apiv3 import fyersModel


client_id = "XC4XXXXM-100"
access_token = "eyJ0eXXXXXXXX2c5-Y3RgS8wR14g"

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,is_async=False, log_path="")


data = {
    "symbol":"MCX:SILVERMIC20NOVFUT",
    "positionSide":1,
    "convertQty":1,
    "convertFrom":"INTRADAY",
    "convertTo":"CNC"
}

response = fyers.convert_position(data=data)
print(response)