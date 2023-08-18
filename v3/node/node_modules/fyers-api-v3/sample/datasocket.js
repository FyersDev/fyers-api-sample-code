let DataSocket = require("../index.js").fyersDataSocket;

var skt= DataSocket.getInstance("")

skt.on("connect",function(){skt.subscribe(['NSE:IDEA-EQ',"NSE:SBIN-EQ"],false,1)
skt.mode(skt.FullMode,1)
console.log(skt.isConnected())
// skt.mode(skt.LiteMode,[11,12,13])
// skt.channelresume(2)
// skt.unsubscribe(['NSE:IDEA-EQ'],false,1)
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