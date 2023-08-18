moduleName = "getAccessToken"
"""
    1.We need to first install fyers-apiv2(can be installed as 'pip install fyers-apiv2)
    2.We then need to import accesToken module from fyers_api directory(as done below)
    3.We also need to import webbrowser to preform an action while generating authcode
"""
from fyers_api import fyersModel
import webbrowser


def getauthToken(appId, redirect_uri):
    functionName = "getauthToken"
    """
        :param app_id: "XXXXXXXXXXX"
        :param redirect_url: "https://XXXXXX.com"
		 1. This function open this url in the browser.
		 2. This will ask you to login and will ask you to approve the app if it is not approved already.
		 3. Once that is done, it will redirect to a url (added while app creation) with the auth_code. The url will look like
		    https://www.google.com/?auth_code=eyJ0eXAiOiXXXXXGciOiJIUzI1NiJ9.eyXXXXXXXXXXXXXInN1YiI6ImF1dGhDb2XXXXXXXXXXXXXXXXXX2lkIjoiQjhQV0xWSDhUNiIsImlzcyI6ImFwaS5sb2dpbi5meWVycy5pbiIsImF1ZCI6WyJ4OjAiLCJ4OjEiLCJ4OjIiXSwidXVpZCI6ImZhOGNhYjE3ZWU4OTQzMGRhZjA1YWUxNDI2YWVkYzI4IiwiaXBBZGRyIjoiMjIzLjIzMy40Mi40NiIsImRpc3BsYXlfbmFtZSI6IkRQMDA0MDQiLCJpYXQiOjE1OTM1ODYzNzEsIm5iZiI6MTU5MzU4NjM3MX0.IMJHzQGHQgyXt_XN0AgDrMN1keR4qolFFKO6cyXTnTg&user_id=DP00404
		 4. You have to take the auth_code from the url and use that token in your generate_access_token function.
	"""
    response_type="code"
    grant_type="authorization_code"
    # creating an instance appSession to generate the auth code by passing app id and redirect url as parameter
    appSession = fyersModel.SessionModel(client_id=appId,redirect_uri=redirect_uri,response_type=response_type, grant_type=grant_type,state="state",scope="",nonce="")

    # The variable `generateTokenUrl` will have a url like https://uat-api.fyers.in/api/dev/generate-authcode?appId=B8PXXXH8T6&redirectUrl=https%3A%2F%2Fgoogle.com
    generateTokenUrl = appSession.generate_authcode()

    # This command is used to open the url in default system brower
    webbrowser.open(generateTokenUrl, new=1)


def generate_access_token(auth_code, appId, secret_key):
    functionName = "generate_access_token"
    """
	:param auth_code: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTM1ODY2NzEsInN1YiI6ImF1dGhDb2RlIiwiYXBwX2lkIjoiQjhQV0xWSDhUNiIsImlzcyI6ImFwaS5sb2dpbi5meWVycy5pbiIsImF1ZCI6WyJ4OjAiLCJ4OjEiLCJ4OjIiXSwidXXXXXXXXXXXYjE3ZWU4OTQzMGRhZjA1YWUxNDI2YWVkYzI4IiwiaXBBZGRyIjoiMjIzLjIzMy40Mi40NiIsImRpc3BsYXlfbmFtZSI6IkRQMDA0MDQiLCJpYXQiOjE1OTM1ODYzNzEsIm5iZiI6MTU5MzU4NjM3MX0.IMJHzQGHQgyXt_XN0AgDrMN1keR4qolFFKO6cyXTnTg"
	:param app_id: "B8PXXXXXXX"
	:param secret_key: "XXXXXXKGN0"
	:param redirect_url: "https://XXXXXX.com"
	:return: access_token: "eyJ0eXAiOiJKV1QiLCXXXX1NiJ9.eyJpYXXXXXXXXXXMsIm5iZiI6MTU5MzU4ODM3MywiZXhwIjoxNTkzNjQ5ODEzLCJpc3MiOiJhcGkuZnllcnMuaW4iLCJzdWIiOiJhY2Nlc3MiLCJhdWQiOiJ4OjAseDoxLHg6MiIsImF0X2hhc2giOiJnQUFBQUFCZV9EcVZIZExMMTAzTVpVN1NYSkZfR2p5R3hidzMtTVVhb0VEMGI0QUVvNjFsR24tREY2OFU5cXhuNzd0UXVoOVVJalYtNm9MVXhINVFfWE1WTEJfRXpROGV2clJmUzlNUXB0Y2J5c2ltN1drWllZTT0iLCJkaXNwbGF5X25hbWUiOiJQSVlVU0ggUkFKRU5EUkEgS0FQU0UiLCJmeV9pZCI6IkRQMDA0MDQifQ.cAfrj2TxAyb8A_9DfiCb1hLIZg_mH-xvP3Ybnj3a4AE"

	1.this function takes the param and return the access_token
	2.the access_token created will be used further .(in fyersModel)]
	3. one can get the auth_code from the url generated by getauthToken function (from auth_code= ..... &user_Id=xxxxxx before &)
	"""
    # creating an instance appSession by passing app id,secret key and redirect url as parameter
    appSession = fyersModel.SessionModel(client_id=appId, secret_key=secret_key,grant_type="authorization_code")

    # we need to pass the auth code in set_token method
    appSession.set_token(auth_code)
    # generate_token function will return us the access token and we store in variable "access_token"
    access_token = appSession.generate_token()
    return access_token


def main():
    """
    Starting Steps.
    1.We first need to uncomment the function getauthToken(appId, redirect_url).
    2.We need to make sure generate_access_token(auth_code, appId, app_secret, redirect_url) func is commented.
    3.We need to run this module code once passing the parameters to getauthToken(appId, redirect_url) func.
    4.We copy the auth_code provided from our browser and store in the variable in "auth_code".
    5.Next we need to uncomment the function generate_access_token(auth_code, appId, app_secret, redirect_url).
    6.Then we need to make sure getauthToken(appId, redirect_url) func is commented.
    7.We run this module again with appropriate parameters.
    """
    # The provided redirct url while creating the app
    redirect_url = "https://www.google.com/"

    # The app id we get after creating the app
    appId = "OCDXXXXXXJ-100"

    # Function to get the auth code and need to be commented while calling the generate_access_token(x,x,x) func.
    getauthToken(appId, redirect_url)




    # The app secret we got after creating the app.
    app_secret = "BXXXXFM90"

    # the genarted auth code we got from browser after running the getauthToken(x,x) func.
    auth_code = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJpYXQiOjE2OTA4NjQwOTAsImV4cCI6MTY5MDg5NDA5MCwibmJmIjoxNjkwODYzNDkwLCJhdWQiOiJbXCJ4OjBcIiwgXCJ4OjFcIiwgXCJ4OjJcIiwgXCJkOjFcIiwgXCJkOjJcIiwgXCJ4OjFcIiwgXCJ4OjBcIl0iLCJzdWIiOiJhdXRoX2NvZGUiLCJkaXNwbGF5X25hbWUiOiJYVjIwOTg2Iiwib21zIjoiSzEiLCJoc21fa2V5IjoiMGE1NTY1NGRhOWRjODUzMTExYzdhYzI0NjM2ZTkyNTQxMTEwYjdjNTJjYzVjYmQxNDAwNjkwNTciLCJub25jZSI6ImJha2EiLCJhcHBfaWQiOiJYQzRFT0Q2N0lNIiwidXVpZCI6IjhjOWEzYjc3YTA3ZDRhNDVhODJiZTI2MjVlMjk3NzgzIiwiaXBBZGRyIjoiMC4wLjAuMCIsInNjb3BlIjoiIn0.31CfyL7lnN5ZEU2-cRjtt8UP3carqt3Vk4YEPNaSBxE"

    # Function to get the access token and need to be commented while calling the getauthToken(x,x) func.
    print(generate_access_token(auth_code, appId, app_secret))


if __name__ == '__main__':
    main()