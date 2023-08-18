"use strict";

var fyersModel =require("./apiService/apiService.js");
var fyersDataSocket =require("./HSM/datasocket.min.js");
var fyersOrderSocket =require("./ordersocket/fyersSocket.js");

module.exports.fyersModel = fyersModel;
module.exports.fyersDataSocket = fyersDataSocket;
module.exports.fyersOrderSocket = fyersOrderSocket;