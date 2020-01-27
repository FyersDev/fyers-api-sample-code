const fyers = require("fyers-api")
const opn = require("opn")

let app_id = "XXXX"
let app_secret = "XXXX"

let reqBody = {"app_id":app_id, "secret_key":app_secret}
let result = fyers.auth(reqBody)
result.then(function(resp){
	if(resp.code != 200){
		console.log(resp);
		process.exit();
	}

	let auth_code = resp.data.authorization_code

	var url = fyers.generateToken()
	opn(url)
}).catch(function(err){
	console.log("unexpected error "+err)
	process.exit()
})