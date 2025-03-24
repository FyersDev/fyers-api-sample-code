const FyersAPI = require("fyers-api-v3").fyersModel


var fyers = new FyersAPI({ path: "/path/to/where/logs/to/be/saved" })
// set appID
fyers.setAppId("Qxxxxxx75-1xx")

// set redirectURL
fyers.setRedirectUrl("https://XXXXX.com")

// set accessToken
fyers.setAccessToken("eyJ0xxxx")

var inp={
    "exit_all":1
}

fyers.exit_position(inp).then((response) => {
    console.log(response)
}).catch((error) => {
    console.log(error)
})