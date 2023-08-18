var fyersOrderSocket= require("../index.js").fyersOrderSocket

var skt=new fyersOrderSocket("")

skt.on("error",function (errmsg) {
    console.log(errmsg)
})
skt.on('general',function (msg) {
    console.log(msg)
})
skt.on('connect',function () {
    skt.subscribe([skt.orderUpdates,skt.tradeUpdates,skt.positionUpdates,skt.edis,skt.pricealerts])
    console.log(skt.isConnected())
})
skt.on('close',function () {
    console.log('closed')
})
skt.on('orders',function (msg) {
    console.log("orders",msg)
})
skt.on('trades',function (msg) {
    console.log('trades',msg)
})
skt.on('positions',function (msg) {
    console.log('positions',msg)
})
skt.autoreconnect()
skt.connect()

