"use strict";
let { Config } = require("../config/config");
let errorHandler = require("../errorHandler/errorHandler");
let axios = require("axios")
const crypto = require('crypto');
let Logger = require("../logger/log.js")

/**
 * Class to access Fyers API.
 * @class
 */
class FyersApi {
    /**
     * Create a new DataSocket object to acess symboldata websocket.
     * @constructor
     * @param {Object} params - The parameters for initializing the DataSocket.
     * @param {string} params.AccessToken - The access token for authentication.
     * @param {string} params.AppID - AppID of user.
     * @param {string} params.RedirectURL - Redirect URL provided while creating the APP.
     * @param {string} [params.Version="2.0"] - the version of API you want your output format in.
     */
    constructor(params) {
        var self = this;

        /**
         * AccessToken of user.
         * @type {String}
         */
        self.AccessToken = params?.AccessToken ?? null;;

        /**
         * RedirectURL of provided by user.
         * @type {String}
         */
        self.RedirectURL = params?.RedirectURL ?? null;

        /**
         * APPID provided by user.
         * @type {String}
         */
        self.AppID = params?.AppID ?? null;
        /**
         * API version provided by client.
         * @type {String}
         */
        self.Version = params?.Version ?? "2.0";

        /**
         * filepath where are logs are to be saved.
         * @type {string}
         */
        self.LogPath = params?.path ?? undefined;

        /**
         * object used to write logs.
         * @type {Logger}
         */
        self.Logger = new Logger(this.LogPath)
    }

    /**
     * sets the APPID.
     * @param {string} req - APPID in format xxxxxx-xxx.
     */
    setAppId = function (req) {
        this.AppID = req
    }

    /**
     * sets the RedirectURL.
     * @param {string} req - pass redirect URL set during creation of APP.
     */
    setRedirectUrl = function (req) {
        this.RedirectURL = req
    }

    /**
     * sets the AccessToken.
     * @param {string} req - pass Access token.
     */
    setAccessToken = function (req) {
        if (this.AppID == null) {
            console.log("Please set APPID using setAppId function")
        }
        else {
            this.AccessToken = this.AppID + ":" + req
        }
    }

    /**
     * get generate-authcode URL to login and generate authcode.
     * @param {Object} req - defines for what the callback function is.
     * @param {string} req.client_id - AppID of user.
     * @param {string} req.redirect_uri - RedirectURL provided by user.
     * @param {string} [req.state] - state value.
     * @returns {string} generate authcode url
     */
    generateAuthCode = function (req) {
        var funcname = 'generateAuthCode'
        var logger = this.Logger
        const client_id = (req && req.client_id) || this.AppID;
        const redirect_uri = (req && req.redirect_uri) || this.RedirectURL;
        const state = (req && req.state) || "sample_state";
        logger.debug('generate authcode response', `${Config.API}generate-authcode?client_id=${client_id}&redirect_uri=${redirect_uri}&response_type=code&state=${state}`, funcname);
        return `${Config.SYNC_API}/generate-authcode?client_id=${client_id}&redirect_uri=${redirect_uri}&response_type=code&state=${state}`
    }

    /**
     * generate access token to use the API's.
     * @param {Object} req - defines for what the callback function is.
     * @param {string} req.client_id - AppID of user.
     * @param {string} req.secret_key - App Secret of user.
     * @param {string} req.auth_code - authcode generated after use of generateAuthCode and login.
     * @param {string} [req.code_verifier] - code verifier.
     * @returns {Object} Object with access token and refresh token if successful
     */
    generate_access_token = async (req) => {
        var funcname = 'generateAuthCode'
        var logger = this.Logger
        const code_verifier = req.code_verifier || "";
        const auth_code = req.auth_code || "";
        const client_id = req.client_id || this.AppID;
        const secret_key = req.secret_key || "";
        const sha256 = getSHA256Hash(`${client_id}:${secret_key}`)
        logger.debug("generate_access_token inputs", { "code_verifier": code_verifier, "auth_code": auth_code, "client_id": client_id, "secret_key": secret_key, "sha256": sha256 }, funcname)
        try {

            if (code_verifier === "") {

                const access_token = await axios.post(`${Config.SYNC_API}/validate-authcode`, {
                    grant_type: "authorization_code",
                    code: req.auth_code,
                    appIdHash: sha256

                })
                return access_token.data;
            }
            else {

                const access_token = await axios.post(`${Config.API}/validate-authcode`, {
                    grant_type: "authorization_code",
                    code_verifier: req.code_verifier,
                    code: req.auth_code,


                })
                return access_token.data;
            }

        }
        catch (e) {
            var err = new errorHandler(e).getError()
            logger.error("error generating access token", err, funcname)
            return err
        }
    }

    /**
     * get profile data.
     * @returns {Promise} returns profile data on resolve or error message and error code on failure
     */
    get_profile = async (req) => {
        var funcname = 'get_profile'
        var logger = this.Logger
        let AuthrizationToken = this.AccessToken
        let vers = this.Version
        return new Promise(async function (resolve, reject) {
            try {
                var url = Config.SYNC_API + Config["get_profile"]
                await axios.get((url), {
                    headers: {
                        Authorization: AuthrizationToken,
                        version: vers
                    }
                })
                    .then(Response => {
                        logger.debug(`${funcname} response`, Response.data, funcname)
                        resolve(Response.data)
                    })
            }
            catch (e) {
                var err = new errorHandler(e).getError()
                logger.error(`${funcname} response`, err, funcname)
                reject(err)
            }
        })
    }

    /**
     * get funds detail.
     * @returns {Promise} returns funds detail on resolve or error message and error code on failure
     */
    get_funds = async (req) => {
        var funcname = 'get_funds'
        var logger = this.Logger
        let AuthrizationToken = this.AccessToken
        let vers = this.Version
        return new Promise(async function (resolve, reject) {
            try {
                var url = Config.SYNC_API + Config["funds"]
                await axios.get((url), {
                    headers: {
                        Authorization: AuthrizationToken,
                        version: vers
                    }
                })
                    .then(Response => {
                        logger.debug(`${funcname} response`, Response.data, funcname)
                        resolve(Response.data)
                    })
            }
            catch (e) {
                var err = new errorHandler(e).getError()
                logger.error(`${funcname} response`, err, funcname)
                reject(err)
            }
        })
    }

    /**
     * get holdings detail.
     * @returns {Promise} returns holdings detail on resolve or error message and error code on failure
     */
    get_holdings = async (req) => {
        var funcname = 'get_holdings'
        var logger = this.Logger
        let AuthrizationToken = this.AccessToken
        let vers = this.Version
        return new Promise(async function (resolve, reject) {
            try {
                var url = Config.SYNC_API + Config["holdings"]
                await axios.get((url), {
                    headers: {
                        Authorization: AuthrizationToken,
                        version: vers
                    }
                })
                    .then(Response => {
                        logger.debug(`${funcname} response`, Response.data, funcname)
                        resolve(Response.data)
                    })
            }
            catch (e) {
                var err = new errorHandler(e).getError()
                logger.error(`${funcname} response`, err, funcname)
                reject(err)
            }
        })
    }


    /**
     * get orderbook to get order details of order placed on current day.
     * @returns {Promise} returns orderbook detail on resolve or error message and error code on failure
     */
    get_orders = async (req) => {
        var funcname = 'get_orders'
        var logger = this.Logger
        let AuthrizationToken = this.AccessToken
        let vers = this.Version
        return new Promise(async function (resolve, reject) {
            try {
                var url = Config.SYNC_API + Config["orders"]
                await axios.get((url), {
                    headers: {
                        Authorization: AuthrizationToken,
                        version: vers
                    }
                })
                    .then(Response => {
                        logger.debug(`${funcname} response`, Response.data, funcname)
                        resolve(Response.data)
                    })
            }
            catch (e) {
                var err = new errorHandler(e).getError()
                logger.error(`${funcname} response`, err, funcname)
                reject(err)
            }
        })
    }

    /**
     * get orderbook for a specific order ID.
     * @param {Object} req - defines for what the callback function is.
     * @param {string} req.order_id - orderID for which orderbook is required for.
     * @returns {Promise} returns orderbook detail of passed order ID on resolve or error message and error code on failure
     */
    get_filtered_orders = async (req) => {
        var funcname = 'get_filtered_orders'
        var logger = this.Logger
        let AuthrizationToken = this.AccessToken
        let vers = this.Version
        return new Promise(async function (resolve, reject) {
            try {
                var url = Config.SYNC_API + Config["orders"] + `?id=${req.order_id}`
                await axios.get((url), {
                    headers: {
                        Authorization: AuthrizationToken,
                        version: vers
                    }
                })
                    .then(Response => {
                        logger.debug(`${funcname} response`, Response.data, funcname)
                        resolve(Response.data)
                    })
            }
            catch (e) {
                var err = new errorHandler(e).getError()
                logger.error(`${funcname} response`, { "Error": err, "inputs": req }, funcname)
                reject(err)
            }
        })
    }

    /**
     * get positionbook to get position details.
     * @returns {Promise} returns positionbook detail on resolve or error message and error code on failure
     */
    get_positions = async (req) => {
        var funcname = 'get_positions'
        var logger = this.Logger
        let AuthrizationToken = this.AccessToken
        let vers = this.Version
        return new Promise(async function (resolve, reject) {
            try {
                var url = Config.SYNC_API + Config["positions"]
                await axios.get((url), {
                    headers: {
                        Authorization: AuthrizationToken,
                        version: vers
                    }
                })
                    .then(Response => {
                        logger.debug(`${funcname} response`, Response.data, funcname)
                        resolve(Response.data)
                    })
            }
            catch (e) {
                var err = new errorHandler(e).getError()
                logger.error(`${funcname} response`, err, funcname)
                reject(err)
            }
        })
    }

    /**
     * get tradebook to get trade details.
     * @returns {Promise} returns tradebook detail on resolve or error message and error code on failure
     */
    get_tradebook = async (req) => {
        var funcname = 'get_tradebook'
        var logger = this.Logger
        let AuthrizationToken = this.AccessToken
        let vers = this.Version
        return new Promise(async function (resolve, reject) {
            try {
                var url = Config.SYNC_API + Config["tradebook"]
                await axios.get((url), {
                    headers: {
                        Authorization: AuthrizationToken,
                        version: vers
                    }
                })
                    .then(Response => {
                        logger.debug(`${funcname} response`, Response.data, funcname)
                        resolve(Response.data)
                    })
            }
            catch (e) {
                var err = new errorHandler(e).getError()
                logger.error(`${funcname} response`, err, funcname)
                reject(err)
            }
        })
    }

    /**
     * use to place order.
     * @param {Object} req - request data.
     * @returns {Promise} returns orderID of placed order on resolve or error message and error code on failure
     */
    place_order = async (req) => {
        var funcname = 'place_order'
        var logger = this.Logger
        let AuthrizationToken = this.AccessToken
        let vers = this.Version
        return new Promise(async function (resolve, reject) {
            try {
                var url = Config.SYNC_API + Config["orders_sync"]
                await axios.post((url), req, {
                    headers: {
                        Authorization: AuthrizationToken,
                        version: vers
                    }
                })
                    .then(Response => {
                        logger.debug(`${funcname} response`, Response.data, funcname)
                        resolve(Response.data)
                    })

            }
            catch (e) {
                var err = new errorHandler(e).getError()
                logger.error(`${funcname} response`, { "Error": err, "inputs": req }, funcname)
                reject(err)
            }
        })
    }

    /**
     * use to place multiple order.
     * @param {Object[]} req - request data.
     * @returns {Promise} returns orderID of all placed and if they are failed or successful on resolve or error message and error code on failure
     */
    place_multi_order = async (req) => {
        var funcname = 'place_multi_order'
        var logger = this.Logger
        let AuthrizationToken = this.AccessToken
        let vers = this.Version
        return new Promise(async function (resolve, reject) {
            try {
                var url = Config.SYNC_API + Config["multi_orders"]
                await axios.post((url), req, {
                    headers: {
                        Authorization: AuthrizationToken,
                        version: vers
                    }
                })
                    .then(Response => {
                        logger.debug(`${funcname} response`, Response.data, funcname)
                        resolve(Response.data)
                    })
            }
            catch (e) {
                var err = new errorHandler(e).getError()
                logger.error(`${funcname} response`, { "Error": err, "inputs": req }, funcname)
                reject(err)
            }
        })
    }

    /**
     * use to modify placed orders which are not traded yet.
     * @param {Object} req - request data.
     * @returns {Promise} returns orderID of passed order ID and if modification was successful or not resolve or error message and error code on failure
     */
    modify_order = async (req) => {
        var funcname = 'modify_order'
        var logger = this.Logger
        let AuthrizationToken = this.AccessToken
        let vers = this.Version
        return new Promise(async function (resolve, reject) {
            try {
                var url = Config.SYNC_API + Config["orders_sync"]
                await axios.patch((url), req, {
                    headers: {
                        Authorization: AuthrizationToken,
                        version: vers
                    }
                })
                    .then(Response => {
                        logger.debug(`${funcname} response`, Response.data, funcname)
                        resolve(Response.data)
                    })
            }
            catch (e) {
                var err = new errorHandler(e).getError()
                logger.error(`${funcname} response`, { "Error": err, "inputs": req }, funcname)
                reject(err)
            }
        })
    }

    /**
     * use to modify multiple placed orders which are not traded yet.
     * @param {Object[]} req - request data.
     * @returns {Promise} returns orderID of passed order ID and if modification was successful or not on resolve or error message and error code on failure
     */
    modify_multi_order = async (req) => {
        var funcname = 'modify_multi_order'
        var logger = this.Logger
        let AuthrizationToken = this.AccessToken
        let vers = this.Version
        return new Promise(async function (resolve, reject) {
            try {
                var url = Config.SYNC_API + Config["multi_orders"]
                await axios.patch((url), req, {
                    headers: {
                        Authorization: AuthrizationToken,
                        version: vers
                    }
                })
                    .then(Response => {
                        logger.debug(`${funcname} response`, Response.data, funcname)
                        resolve(Response.data)
                    })
            }
            catch (e) {
                var err = new errorHandler(e).getError()
                logger.error(`${funcname} response`, { "Error": err, "inputs": req }, funcname)
                reject(err)
            }
        })
    }

    /**
     * use to cancel placed orders which are not traded yet.
     * @param {Object} req - request data.
     * @returns {Promise} returns orderID of passed order ID and if cancellation was successful or not on resolve or error message and error code on failure
     */
    cancel_order = async (req) => {
        var funcname = 'cancel_order'
        var logger = this.Logger
        let AuthrizationToken = this.AccessToken
        let vers = this.Version
        return new Promise(async function (resolve, reject) {
            try {
                var url = Config.SYNC_API + Config["orders_sync"]
                await axios.delete((url), req, {
                    headers: {
                        Authorization: AuthrizationToken,
                        version: vers
                    }
                })
                    .then(Response => {
                        logger.debug(`${funcname} response`, Response.data, funcname)
                        resolve(Response.data)
                    })
            }
            catch (e) {
                var err = new errorHandler(e).getError()
                logger.error(`${funcname} response`, { "Error": err, "inputs": req }, funcname)
                reject(err)
            }
        })
    }

    /**
     * use to cancel multiple placed orders which are not traded yet.
     * @param {Object[]} req - request data.
     * @returns {Promise} returns orderID of passed order ID and if cancellation was successful or not on resolve or error message and error code on failure
     */
    cancel_multi_order = async (req) => {
        var funcname = 'cancel_multi_order'
        var logger = this.Logger
        let AuthrizationToken = this.AccessToken
        let vers = this.Version
        return new Promise(async function (resolve, reject) {
            try {
                var url = Config.SYNC_API + Config["multi_orders"]
                await axios.delete((url), req, {
                    headers: {
                        Authorization: AuthrizationToken,
                        version: vers
                    }
                })
                    .then(Response => {
                        logger.debug(`${funcname} response`, Response.data, funcname)
                        resolve(Response.data)
                    })
            }
            catch (e) {
                var err = new errorHandler(e).getError()
                logger.error(`${funcname} response`, { "Error": err, "inputs": req }, funcname)
                reject(err)
            }
        })
    }

    /**
     * use to exit all positions.
     * @param {Object} req - request data.
     * @returns {Promise} returns success message on resolve or error message and error code on failure
     */
    exit_position = async (req) => {
        var funcname = 'exit_position'
        var logger = this.Logger
        let AuthrizationToken = this.AccessToken
        let vers = this.Version
        return new Promise(async function (resolve, reject) {
            try {
                var url = Config.SYNC_API + Config["positions"]
                await axios.delete((url), {
                    headers: {
                        Authorization: AuthrizationToken,
                        version: vers
                    },
                    data: req
                })
                    .then(Response => {
                        logger.debug(`${funcname} response`, Response.data, funcname)
                        resolve(Response.data)
                    })
            }
            catch (e) {
                var err = new errorHandler(e).getError()
                logger.error(`${funcname} response`, { "Error": err, "inputs": req }, funcname)
                reject(err)
            }
        })
    }

    /**
     * use to convert open positions.
     * @param {Object} req - request data.
     * @returns {Promise} returns success message on resolve or error message and error code on failure
     */
    convert_position = async (req) => {
        var funcname = 'convert_position'
        var logger = this.Logger
        let AuthrizationToken = this.AccessToken
        let vers = this.Version
        return new Promise(async function (resolve, reject) {
            try {
                var url = Config.SYNC_API + Config["positions"]
                await axios.post((url), req, {
                    headers: {
                        Authorization: AuthrizationToken,
                        version: vers
                    }
                })
                    .then(Response => {
                        logger.debug(`${funcname} response`, Response.data, funcname)
                        resolve(Response.data)
                    })
            }
            catch (e) {
                var err = new errorHandler(e).getError()
                logger.error(`${funcname} response`, { "Error": err, "inputs": req }, funcname)
                reject(err)
            }
        })
    }

    /**
     * use to get market status.
     * @returns {Promise} returns success message on resolve or error message and error code on failure
     */
    market_status = async (req) => {
        var funcname = 'market_status'
        var logger = this.Logger
        let AuthrizationToken = this.AccessToken
        let vers = this.Version
        return new Promise(async function (resolve, reject) {
            try {
                var url = Config.data_Api1 + Config["marketStatus"]
                const profile = await axios.get((url), {
                    headers: {
                        Authorization: AuthrizationToken,
                        version: vers
                    }
                })
                    .then(Response => {
                        logger.debug(`${funcname} response`, Response.data, funcname)
                        resolve(Response.data)
                    })
            }
            catch (e) {
                var err = new errorHandler(e).getError()
                logger.error(`${funcname} response`, err, funcname)
                reject(err)
            }
        })
    }

    /**
     * use to get historic data of symbol.
     * @param {Object} req - request data.
     * @returns {Promise} returns success message on resolve or error message and error code on failure
     */
    getHistory = async (req) => {
        var funcname = 'getHistory'
        var logger = this.Logger
        let AuthrizationToken = this.AccessToken
        let vers = this.Version
        return new Promise(async function (resolve, reject) {
            try {
                var url = Config.data_Api1 + Config["history"]
                url = generateUrl(url, req)
                await axios.get((url), {
                    headers: {
                        Authorization: AuthrizationToken,
                        version: vers
                    }
                })
                    .then(Response => {
                        logger.debug(`${funcname} response`, Response.data, funcname)
                        resolve(Response.data)
                    })
            }
            catch (e) {
                var err = new errorHandler(e).getError()
                logger.error(`${funcname} response`, { "Error": err, "inputs": req }, funcname)
                reject(err)
            }
        })
    }

    /**
     * use to get quotes data of symbols.
     * @param {Array} req - array of symbols.
     * @returns {Promise} returns success message on resolve or error message and error code on failure
     */
    getQuotes = async (req) => {
        var funcname = 'getQuotes'
        var logger = this.Logger
        let AuthrizationToken = this.AccessToken
        let vers = this.Version
        return new Promise(async function (resolve, reject) {
            try {
                var url = Config.data_Api1 + Config["quotes"]
                var symbolstring = ""
                req.forEach(function (element) {
                    symbolstring = symbolstring + element + ','
                })
                symbolstring = symbolstring.slice(0, -1)//remove last ','
                var data = { "symbols": symbolstring }
                const urlParams = new URLSearchParams(data);
                url = url + '?' + urlParams
                await axios.get((url), {
                    headers: {
                        Authorization: AuthrizationToken,
                        version: vers
                    }
                })
                    .then(Response => {
                        logger.debug(`${funcname} response`, Response.data, funcname)
                        resolve(Response.data)
                    })
            }
            catch (e) {
                var err = new errorHandler(e).getError()
                logger.error(`${funcname} response`, { "Error": err, "inputs": req }, funcname)
                reject(err)
            }
        })
    }

    /**
     * use to get market depth data of symbols.
     * @param {Array} req - array of symbols.
     * @returns {Promise} returns success message on resolve or error message and error code on failure
     */
    getMarketDepth = async (req) => {
        var funcname = 'getQuotes'
        var logger = this.Logger
        let AuthrizationToken = this.AccessToken
        let vers = this.Version
        return new Promise(async function (resolve, reject) {
            try {
                var url = Config.data_Api1 + Config["market_depth"]
                var symbolstring = ""
                req.symbol.forEach(function (element) {
                    symbolstring = symbolstring + element + ','
                })
                symbolstring = symbolstring.slice(0, -1)//remove last ','
                var data = { "symbol": symbolstring, "ohlcv_flag": req.ohlcv_flag }
                const urlParams = new URLSearchParams(data);
                url = url + '?' + urlParams
                await axios.get((url), {
                    headers: {
                        Authorization: AuthrizationToken,
                        version: vers
                    }
                })
                    .then(Response => {
                        logger.debug(`${funcname} response`, Response.data, funcname)
                        resolve(Response.data)
                    })
            }
            catch (e) {
                var err = new errorHandler(e).getError()
                logger.error(`${funcname} response`, { "Error": err, "inputs": req }, funcname)
                reject(err)
            }
        })
    }
}

function generateUrl(url, queryObject) {
    let finalUrl = url + "?"
    for (let key in queryObject) {
        finalUrl = finalUrl + key + "=" + queryObject[key] + "&"
    }
    return finalUrl.substring(0, finalUrl.length - 1);
}

function getSHA256Hash(inputString) {
    const hash = crypto.createHash('sha256');
    hash.update(inputString);
    return hash.digest('hex');
}
module.exports = FyersApi;