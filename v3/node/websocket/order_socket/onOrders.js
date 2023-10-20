var fyersOrderSocket= require("fyers-api-v3").fyersOrderSocket

// Replace the sample access token with your actual access token
// access_token format will be "APPID:access_token"
// For example : access_token = "7N***X38S-100:eyJ0eXA****************PSv0bLiHOqW5SI"
const accesstoken = "XCXXXXXXM-100:eyJ0tHfZNSBoLo"

var skt=new fyersOrderSocket(accesstoken,"path/where/logs/to/be/saved")

skt.on("error",function (errmsg) {
    console.log(errmsg)
})

//handle your general messages here
skt.on('general',function (msg) {
    console.log(msg)
})
skt.on('connect',function () {
    skt.subscribe([skt.orderUpdates])
    console.log(skt.isConnected())
})

skt.on('close',function () {
    console.log('closed')
})

//handle your order messages here
skt.on('orders',function (msg) {
    console.log("orders",msg)
})

//handle your trade messages here
skt.on('trades',function (msg) {
    console.log('trades',msg)
})

//handle your positions messages here
skt.on('positions',function (msg) {
    console.log('positions',msg)
})

skt.autoreconnect()
skt.connect()

