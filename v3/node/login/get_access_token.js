const FyersAPI = require("fyers-api-v3").fyersModel
const open = require('opn');

var fyers = new FyersAPI({path:"/path/to/where/logs/to/be/saved"})
// set appID
fyers.setAppId("Qxxxxxx75-1xx")

// set redirectURL
fyers.setRedirectUrl("https://XXXXX.com")

var generateAuthcodeURL = fyers.generateAuthCode();

// Open the URL in the default web browser to allow the user to grant access
open(generateAuthcodeURL)
  .then(() => {
    console.log(`Opened ${generateAuthcodeURL} in your default web browser.`);
  })
  .catch((error) => {
    console.error('Error occurred:', error);
  });


// Define the authorization code and secret key required for generating access token
const auth_code="exyj....."
// Replace with your secret key provided by Fyers
const secretKey = "RJ1W2XG5L4"

// fyers.generate_access_token({ "secret_key": secretKey, "auth_code": auth_code }).then((response) => {
//     console.log(response)
// }).catch((error) => {
//     console.log(error)
// })