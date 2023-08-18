const WebSocket = require('ws');
let Logger = require("../logger/log.js")
let { Config } = require("../config/config");
let mapper =require("./mapper.js")
var reconnectiontries = 0
const maxreconnectiontries = 5
const ordstatobj={11: 4, 12: 4, 20: 4, 21: 4, 22: 6, 23: 6, 24: 6, 25: 6, 26: 6, 90: 2,
    91: 1, 92: 5, 93: 5, 94: 5, 51: 6, 52: 6, 53: 6, 54: 6, 55: 6, 61: 6, 62: 6, 63: 6,
    64: 6, 71: 6, 72: 6, 73: 1}
function datamapper(a,b){
    const result = {};

    for (const key of Object.keys(b)) {
      if (a.hasOwnProperty(key)) {
        result[b[key]] = a[key];
      }
    }
  
    return result;
}
/**
 * Class to access order update websocket.
 * @class
 */
class FyersOrderSocket {
    constructor(authorizationKey, logpath = undefined) {
        this.url = Config.Order_SOCKET;
        this.authorizationKey = authorizationKey;
        this.ws = null;
        this.onErrorCallback = null;
        this.onCloseCallback = null;
        this.onMessageCallback = null;
        this.onOpenCallback = null;
        this.orderscallback = null;
        this.LogPath = logpath;
        this.Logger = new Logger(this.LogPath);
        this.positionscallback = null;
        this.tradescallback = null;
        this.isPingEnabled = true;
        this.pingInterval = null;
        this.autoreconnectinterval = null;
        this.orderUpdates = "orders"
        this.tradeUpdates = "trades"
        this.positionUpdates = "positions"
        this.edis="edis"
        this.pricealerts="pricealerts"
    }

    /**
     * called to connect to the order socket
     */
    connect() {
        const funcname = "connect"
        const logger = this.Logger
        try {
            logger.debug("initalizing connection to socket", { "accesstoken": this.authorizationKey }, funcname)
            this.ws = new WebSocket(this.url, {
                headers: {
                    Authorization: this.authorizationKey,
                },
            });
            this.ws.binaryType = 'arraybuffer';
            this.ws.on('error', (error) => {
                if (this.onErrorCallback) {
                    this.onErrorCallback(error);
                }
                else {
                    console.log("error occoured", error)
                }
            });

            this.ws.on('close', (event) => {
                this.stopPing()
                if (this.onCloseCallback) {
                    this.onCloseCallback(event);
                }
                else {
                    console.log("ws closed", event)
                }
            });

            this.ws.on('message', (message) => {
                const data = message.toString();
                if (data === 'pong') {
                    return
                }
                else {
                    var parseddata = JSON.parse(data)
                    if (parseddata.hasOwnProperty("orders")) {
                        var orderdata=datamapper(parseddata["orders"],mapper.orders)
                        orderdata.status=ordstatobj[orderdata.status]
                        orderdata['orderNumStatus']=orderdata.id+':'+orderdata.status
                        if (this.orderscallback) {
                            this.orderscallback({"s":"ok","orders":orderdata})
                        }
                        else {
                            console.log("Orders_internal", {"s":"ok","orders":orderdata})
                        }
                    }
                    else if (parseddata.hasOwnProperty("positions")) {
                        var positiondata=datamapper(parseddata["positions"],mapper.position)
                        if (this.positionscallback) {
                            this.positionscallback({"s":"ok","positions":positiondata})
                        }
                        else {
                            console.log("positions_internal", {"s":"ok","positions":positiondata})
                        }
                    }
                    else if (parseddata.hasOwnProperty("trades")) {
                        var tradebookdata=datamapper(parseddata["trades"],mapper.tradebook)
                        if (this.tradescallback) {
                            this.tradescallback({"s":"ok","trades":tradebookdata})
                        }
                        else {
                            console.log("trades_internal", {"s":"ok","trades":tradebookdata})
                        }
                    }
                    else {
                        if (this.onMessageCallback) {
                            this.onMessageCallback(parseddata);
                        }
                        else {
                            console.log("message_internal", parseddata)
                        }
                    }

                }
            });

            this.ws.on('open', () => {
                reconnectiontries = 0
                if (this.onOpenCallback) {
                    this.onOpenCallback();
                }
                else {
                    console.log("connected")
                }

                if (this.isPingEnabled) {
                    this.startPing();
                }
            });
        }
        catch (error) {
            console.log(`Error occured ${funcname}: ${error}`)
            logger.error("unexpected error on connect function", error, funcname)
        }
    }

    /**
     * used to define onmessage,onerror,onopen,onclose for websocket.
     * @param {string} onwhat - defines for what the callback function is.
     * @param {Function} callback - the callback function.
     * @throws  error message if onwhat is not valid.
     */
    on(onwhat, callback) {
        const funcname = "on"
        const logger = this.Logger
        try {
            if (onwhat === 'error') {
                this.onErrorCallback = callback;
            }
            else if (onwhat === 'general') {
                this.onMessageCallback = callback;
            }
            else if (onwhat === 'connect') {
                this.onOpenCallback = callback;
            }
            else if (onwhat === 'close') {
                this.onCloseCallback = callback;
            }
            else if (onwhat === 'orders') {
                this.orderscallback = callback;
            }
            else if (onwhat === 'trades') {
                this.tradescallback = callback;
            }
            else if (onwhat === 'positions') {
                this.positionscallback = callback;
            }
            else {
                console.log("incorrect value passed", onwhat)
                logger.error("wrong onwhat passed", { "onwhat": onwhat }, funcname)
            }
        }
        catch (error) {
            logger.error("unexpected error on 'on' function", error, funcname)
        }
    }

    /**
     * call to check if datasocket is connected
     */
    isConnected() {
        return this.ws && this.ws.readyState === WebSocket.OPEN;
    }

    /**
     * starts ping messages to ws
     */
    startPing() {
        this.pingInterval = setInterval(() => {
            if (this.isConnected()) {
                this.ws.send("ping");
            }
        }, 1000);
    }

    /**
     * stops pinging mechanism
     */
    stopPing() {
        clearInterval(this.pingInterval);
    }

    /**
     * Subscribe to socket.
     * @param {Array|string} towhat - array or string of what you want to subscribe to.
     */
    subscribe(towhat) {
        const funcname = "subscribe"
        const logger = this.Logger
        try {
            if (this.isConnected()) {
                logger.debug("trying to subscribe to", { "towhat": towhat }, funcname)
                if (towhat.constructor === Array) {
                    this.ws.send(JSON.stringify({ "T": "SUB_ORD", "SLIST": towhat, "SUB_T": 1 }));
                }
                else {
                    this.ws.send(JSON.stringify({ "T": "SUB_ORD", "SLIST": [towhat], "SUB_T": 1 }));
                }
            }
            else {
                logger.error("websocket is not connected", { "towhat": towhat }, funcname)
                console.log('Cannot send message. WebSocket is not connected.');
            }
        }
        catch (error) {

            logger.error("unexpected error on subscribe function", error, funcname)
        }
    }

    /**
     * Unsubscribe to socket.
     * @param {Array|string} towhat - array or string of what you want to unsubscribe to.
     */
    unsubscribe(towhat) {
        const funcname = "unsubscribe"
        const logger = this.Logger
        try {
            if (this.isConnected()) {
                if (towhat.constructor === Array) {
                    logger.debug("trying to unsubscribe to", { "towhat": towhat }, funcname)
                    this.ws.send(JSON.stringify({ "T": "SUB_ORD", "SLIST": towhat, "SUB_T": -1 }));
                }
                else {
                    this.ws.send(JSON.stringify({ "T": "SUB_ORD", "SLIST": [towhat], "SUB_T": -1 }));
                }
            }
            else {
                logger.error("websocket is not connected", { "towhat": towhat }, funcname)
                console.log('Cannot send message. WebSocket is not connected.');
            }
        }
        catch (error) {
            logger.error("unexpected error on unsubscribe function", error, funcname)
        }
    }

    /**
     * call to close the datasocket.
     */
    close() {
        if (this.ws && this.isConnected) {
            clearInterval(this.autoreconnectinterval)
            this.stopPing()
            this.ws.close();
        }
    }

    /**
     * call to enable autoreconnect functionality of websocket.
     */
    autoreconnect() {
        this.autoreconnectinterval = setInterval(() => {
            if ((!this.isConnected()) && (reconnectiontries < maxreconnectiontries)) {
                console.log("trying to reconnect ", reconnectiontries + 1)
                reconnectiontries++
                this.connect()
            } else if (reconnectiontries >= maxreconnectiontries) {
                console.log("max autoconnect tries exceeded")
                clearInterval(this.autoreconnectinterval)
                this.stopPing()
                reconnectiontries = 0
            }
        }, 5000);

    }
}

module.exports = FyersOrderSocket