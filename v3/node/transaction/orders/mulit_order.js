const FyersAPI = require("fyers-api-v3").fyersModel


var fyers = new FyersAPI({ path: "/path/to/where/logs/to/be/saved" })
// set appID
fyers.setAppId("Qxxxxxx75-1xx")

// set redirectURL
fyers.setRedirectUrl("https://XXXXX.com")

// set accessToken
fyers.setAccessToken("eyJ0xxxx")

var inp=[{
    "symbol":"NSE:SBIN-EQ",
    "qty":1,
    "type":2,
    "side":1,
    "productType":"INTRADAY",
    "limitPrice":0,
    "stopPrice":0,
    "validity":"DAY",
    "disclosedQty":0,
    "offlineOrder":False,
},
{
    "symbol":"NSE:IDEA-EQ",
    "qty":1,
    "type":2,
    "side":1,
    "productType":"INTRADAY",
    "limitPrice":0,
    "stopPrice":0,
    "validity":"DAY",
    "disclosedQty":0,
    "offlineOrder":False,
},{
    "symbol":"NSE:SBIN-EQ",
    "qty":1,
    "type":2,
    "side":1,
    "productType":"INTRADAY",
    "limitPrice":0,
    "stopPrice":0,
    "validity":"DAY",
    "disclosedQty":0,
    "offlineOrder":False,
},
{
    "symbol":"NSE:IDEA-EQ",
    "qty":1,
    "type":2,
    "side":1,
    "productType":"INTRADAY",
    "limitPrice":0,
    "stopPrice":0,
    "validity":"DAY",
    "disclosedQty":0,
    "offlineOrder":False,
}]

fyers.place_multi_order(inp).then((response) => {
    console.log(response)
}).catch((error) => {
    console.log(error)
})