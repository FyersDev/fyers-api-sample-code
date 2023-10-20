const FyersAPI = require("fyers-api-v3").fyersModel


var fyers = new FyersAPI({path:"/path/to/where/logs/to/be/saved"})
// set appID
fyers.setAppId("Qxxxxxx75-1xx")

// set redirectURL
fyers.setRedirectUrl("https://XXXXX.com")

// set accessToken
fyers.setAccessToken("eyJ0xxxx")


var inp={
    "symbol":"NSE:SBIN-EQ",
    "resolution":"D",
    "date_format":"0",
    "range_from":"1622097600",
    "range_to":"1622097685",
    "cont_flag":"1"
}

fyers.getHistory(inp).then((response) => {
    console.log(response)
}).catch((error) => {
    console.log(error)
})