# Fyers-Trading-APIs-Sample-Code
This is the sample code to get started with the fyers trading apis.

###### getAccessToken.py
Just replace of app_id and app_secret in place of "XXXX" and run the code.
The file open the browser with the url like 
	https://api.fyers.in/api/v1/genrateToken?authorization_code=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqaGdqZzg3NiQ3ODVidjVANjQ3NTZ2NSZnNyM2OTg3Njc5OHhkIjoiWElHVFVYVjBSSSIsImV4cCI6MTU2MTU5NzM5Ny41NjQxNTV9.Agl-UUs63NforrUEdbG7YUlPcbFXu9hLYm4akGuIBkU&appId=Your_app_id"
	 1. This will ask you to login and will ask you to approve the app if it is not approved already.
	 2. Once that is done, it will redirect to a url (added while app creation) with the access_token. The url will look like
	    http://localhost:5000?access_token=gAAAAABc3Sh9QpE5mNx2mSz6vvvT29SAsELqkfbKQKa2977zHw3NdPBhe6jAZCBumHvYUum87j53-AzMEPXMjQw31wkRviZ1TdM5OimgTYWEEorWDmWuHnY=&user_id=FYXXXX
	 3. You have to take the access_token from the url and use that token in your going forward.

###### apiCalls.py
Add the access_token generated from the previous file and run the code.
