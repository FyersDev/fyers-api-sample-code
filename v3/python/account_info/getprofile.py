from fyers_apiv3 import fyersModel

client_id = "XC4XXXXM-100"
access_token = "eyJ0eXXXXXXXX2c5-Y3RgS8wR14g"

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")

# Make a request to get the user profile information
response = fyers.get_profile()

# Print the response received from the Fyers API
print(response)

