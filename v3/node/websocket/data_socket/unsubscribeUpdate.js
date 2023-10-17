const DataSocket = require("fyers-api-v3").fyersDataSocket

// Replace the sample access token with your actual access token
// access_token format will be "APPID:access_token"
// For example : access_token = "7N***X38S-100:eyJ0eXA****************PSv0bLiHOqW5SI"
const accesstoken = "XCXXXXXXM-100:eyJ0tHfZNSBoLo"

var skt= DataSocket.getInstance(accesstoken,"path/where/logs/to/be/saved")

skt.on("connect",function(){
skt.subscribe(['NSE:IDEA-EQ',"NSE:SBIN-EQ"])
console.log(skt.isConnected())
})

skt.on("message",function(message){
	if(message.ltp>100 &&message.symbol=="NSE:SBIN-EQ"){
        fyersdata.unsubscribe(["NSE:SBIN-EQ"],false)
    }
})

skt.on("error",function(message){
	console.log("erroris",message)
})

skt.on("close",function(){
    console.log("socket closed")
})
skt.connect()
skt.autoreconnect()