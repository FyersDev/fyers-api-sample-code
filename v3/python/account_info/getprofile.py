from fyers_apiv3 import fyersModel

client_id = "XC4XXXXM-100"
access_token = "eyJ0eXXXXXXXX2c5-Y3RgS8wR14g"

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")

# Make a request to get the user profile information
response = fyers.get_profile()

# Print the response received from the Fyers API
print(response)



{
   "s":"ok",
   "code":200,
   "message":"",
   "data":{
      "fy_id":"XXXXX86",
      "name":"VINAY",
      "image":"https://fyers-user-details.s3.amazonaws.com/image/FK6107548224?X-Amz-Algorithm=AWS4-HMAC",
      "display_name":"VKM",
      "pin_change_date":"15-12-2022 09:24:05",
      "email_id":"xxxnayxm@gmxxl.com",
      "pwd_change_date":"None",
      "PAN":"XXXXXXXXXX",
      "mobile_number":"9XXXXX678",
      "totp":true,
      "pwd_to_expire":90
   }
}