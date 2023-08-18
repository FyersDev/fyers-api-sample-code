const DataSocket = require("fyers-api-v3").fyersDataSocket

var skt= DataSocket.getInstance("accesstoken","path/where/logs/to/be/saved")

skt.on("connect",function(){
skt.subscribe(['NSE:IDEA-EQ',"NSE:SBIN-EQ"])
skt.mode(skt.LiteMode)
// incase of going back to full mode use
// skt.mode(skt.FullMode)

console.log(skt.isConnected())
})

skt.on("message",function(message){
	console.log({"TEST":message})
})

skt.on("error",function(message){
	console.log("erroris",message)
})

skt.on("close",function(){
    console.log("socket closed")
})
skt.connect()
skt.autoreconnect()