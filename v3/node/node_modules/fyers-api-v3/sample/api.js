var fyersModel= require("../index.js").fyersModel

var fyers= new fyersModel()

fyers.setAppId("QCxxxx25-1xx")

fyers.setRedirectUrl("https://xxx.xxxxxxx.xxxx")
// generate authcode
////////////////////////////

// var URL=fyers.generateAuthCode()

// console.log(URL)

// after getting authcode

////////////////////////////

// generate accesstoken
////////////////////////////
// var authcode=""

// fyers.generate_access_token({"client_id":fyers.AppID,"secret_key":"4362L6SS2C","auth_code":authcode}).then((response)=>{
//     console.log(response)
// })
////////////////////////////

fyers.setAccessToken("")

fyers.get_profile().then((response)=>{
        console.log(response)
    }).catch((err)=>{
        console.log(err)
    })
    
fyers.getQuotes(["NSE:SBIN-EQ","NSE:TCS-EQ"]).then((response)=>{
    console.log(response)
}).catch((err)=>{
    console.log(err)
})

fyers.getMarketDepth({"symbol":["NSE:SBIN-EQ","NSE:TCS-EQ"],"ohlcv_flag":1}).then((response)=>{
    console.log(response)
}).catch((err)=>{
    console.log(err)
})