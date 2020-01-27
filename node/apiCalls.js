const fyers = require("fyers-api")

let access_token = "your_access_token_from_url="
fyers.get_profile({token:access_token})
.then(function(resp){
	console.log(resp);
})
.catch(function(err){
	console.log("unexpected error")
	process.exit()
})