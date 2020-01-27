import sys
import webbrowser
from fyers_api import accessToken


def getToken(app_id, app_secret):
	"""
	The variable `generateTokenUrl` will have a url like 
	https://api.fyers.in/api/v1/genrateToken?authorization_code=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqaGdqZzg3NiQ3ODVidjVANjQ3NTZ2NSZnNyM2OTg3Njc5OHhkIjoiWElHVFVYVjBSSSIsImV4cCI6MTU2MTU5NzM5Ny41NjQxNTV9.Agl-UUs63NforrUEdbG7YUlPcbFXu9hLYm4akGuIBkU&appId=Your_app_id"
	 1. This function open this url in the browser. 
	 2. This will ask you to login and will ask you to approve the app if it is not approved already.
	 3. Once that is done, it will redirect to a url (added while app creation) with the access_token. The url will look like
	    http://localhost:5000?access_token=gAAAAABc3Sh9QpE5mNx2mSz6vvvT29SAsELqkfbKQKa2977zHw3NdPBhe6jAZCBumHvYUum87j53-AzMEPXMjQw31wkRviZ1TdM5OimgTYWEEorWDmWuHnY=&user_id=FYXXXX
	 4. You have to take the access_token from the url and use that token in your going forward.
	"""
	appSession = accessToken.SessionModel(app_id,app_secret)

	response = appSession.auth()

	if response["code"] != 200:
		print response
		sys.exit()

	auth_code = response["data"]["authorization_code"]

	appSession.set_token(auth_code)

	generateTokenUrl = appSession.generate_token()
	webbrowser.open(generateTokenUrl,new=1)





def main():
	app_id = "XXXX"
	app_secret = "XXXX"
	getToken(app_id, app_secret)

if __name__ == '__main__':
	main()