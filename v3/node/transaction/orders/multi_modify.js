const FyersAPI = require("fyers-api-v3").fyersModel


var fyers = new FyersAPI({ path: "/path/to/where/logs/to/be/saved" })
// set appID
fyers.setAppId("Qxxxxxx75-1xx")

// set redirectURL
fyers.setRedirectUrl("https://XXXXX.com")

// set accessToken
fyers.setAccessToken("eyJ0xxxx")

var inp=[{
  "id": "8102710298291",
  "type": 1,
  "limitPrice": 61049,
  "qty": 1
},
{
  "id": "8102710298292",
  "type": 1,
  "limitPrice": 61049,
  "qty": 1
}]

fyers.modify_multi_order(inp).then((response) => {
    console.log(response)
}).catch((error) => {
    console.log(error)
})