import sys
from fyers_api import fyersModel

def main():
	access_token = "your_access_token_from_url" ## access_token from the redirect url
	## If you want to make asynchronous API calls then assign the below variable as True and then pass it in the functions, by default its value is False
	# is_async = True
	fyers = fyersModel.FyersModel()
	print(fyers.get_profile(token=access_token))

if __name__ == '__main__':
	main()