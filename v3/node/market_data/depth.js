const FyersAPI = require("fyers-api-v3").fyersModel


var fyers = new FyersAPI({path:"/path/to/where/logs/to/be/saved"})
// set appID
fyers.setAppId("Qxxxxxx75-1xx")

// set redirectURL
fyers.setRedirectUrl("https://XXXXX.com")

// set accessToken
fyers.setAccessToken("eyJ0xxxx")

var inp={"symbol":["NSE:SBIN-EQ","NSE:TCS-EQ"],"ohlcv_flag":1}

fyers.getMarketDepth(inp).then((response) => {
    console.log(response)
}).catch((error) => {
    console.log(error)
})