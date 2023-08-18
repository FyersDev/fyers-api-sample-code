const DataSocket = require("fyers-api-v3").fyersDataSocket

var skt= DataSocket.getInstance("accesstoken","path/where/logs/to/be/saved")

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