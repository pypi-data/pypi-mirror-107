export default class CxSocket {
  websocketStringMessageType: number;
  websocketIntMessageType: number;
  websocketBoolMessageType: number;
  websocketJSONMessageType: number;
  websocketMessagePrefix: string;
  websocketMessageSeparator: string;
  websocketMessagePrefixLen: number;
  websocketMessageSeparatorLen: number;
  websocketMessagePrefixAndSepIdx: number;
  websocketMessagePrefixIdx: number;
  websocketMessageSeparatorIdx: number;
  connectListeners: Array<any>;
  disconnectListeners: Array<any>;
  nativeMessageListeners: Array<any>;
  messageListeners: object;
  conn: WebSocket;
  isReady: boolean;

  constructor(endpoint, protocols, prefix) {
    const _this = this
    this.isReady = false
    this.websocketMessagePrefix = prefix
    this.websocketStringMessageType = 0
    this.websocketIntMessageType = 1
    this.websocketBoolMessageType = 2
    this.websocketJSONMessageType = 4
    this.websocketMessageSeparator = ";"
    this.websocketMessagePrefixLen = this.websocketMessagePrefix.length
    this.websocketMessageSeparatorLen = this.websocketMessageSeparator.length
    this.websocketMessagePrefixAndSepIdx = this.websocketMessagePrefixLen + this.websocketMessageSeparatorLen - 1
    this.websocketMessagePrefixIdx = this.websocketMessagePrefixLen - 1
    this.websocketMessageSeparatorIdx = this.websocketMessageSeparatorLen - 1

    this.connectListeners = []
    this.disconnectListeners = []
    this.nativeMessageListeners = []
    this.messageListeners = {}

    if (!window.WebSocket) {
      return
    }
    if (!endpoint.includes("ws")) {
      endpoint = "ws://" + endpoint
    }
    if (protocols != null && protocols.length > 0) {
      this.conn = new WebSocket(endpoint, protocols)
    } else {
      this.conn = new WebSocket(endpoint)
    }

    this.conn.onopen = function (evt) {
      _this.fireConnect()
      _this.isReady = true
      return null
    }
    this.conn.onclose = function (evt) {
      _this.fireDisconnect()
      return null
    }
    this.conn.onmessage = function (evt) {
      // console.log("onmessage")
      _this.messageReceivedFromConn(evt)
    }
  }

  forceStringMessageType() {
    this.websocketJSONMessageType = this.websocketStringMessageType
  }

  isNumber(obj) {
    return !isNaN(obj - 0) && obj !== null && obj !== "" && obj !== false
  }

  isString(obj) {
    return Object.prototype.toString.call(obj) === "[object String]"
  }

  isBoolean(obj) {
    return typeof obj === "boolean" ||
      (typeof obj === "object" && typeof obj.valueOf() === "boolean")
  }

  isJSON(obj) {
    return typeof obj === "object"
  }

  _msg(event, websocketMessageType, dataMessage) {
    return this.websocketMessagePrefix + ":" + event + this.websocketMessageSeparator + String(websocketMessageType) + this.websocketMessageSeparator + dataMessage
  }

  encodeMessage(event, data) {
    let m = ""
    let t = 0
    if (this.isNumber(data)) {
      t = this.websocketIntMessageType
      m = data.toString()
    } else if (this.isBoolean(data)) {
      t = this.websocketBoolMessageType
      m = data.toString()
    } else if (this.isString(data)) {
      t = this.websocketStringMessageType
      m = data.toString()
    } else if (this.isJSON(data)) {
      // propably json-object
      t = this.websocketJSONMessageType
      m = JSON.stringify(data)
    } else if (data !== null && typeof (data) !== "undefined") {
      // if it has a second parameter but it's not a type we know, then fire this:
      console.log("unsupported type of input argument passed, try to not include this argument to the 'Emit'")
    }
    return this._msg(event, t, m)
  }

  decodeMessage(event, websocketMessage) {
    // iris-websocket-message;user;4;themarshaledstringfromajsonstruct
    const skipLen = this.websocketMessagePrefixLen + this.websocketMessageSeparatorLen + event.length + 2
    if (websocketMessage.length < skipLen + 1) {
      return null
    }
    const websocketMessageType = parseInt(websocketMessage.charAt(skipLen - 2))
    const theMessage = websocketMessage.substring(skipLen, websocketMessage.length)
    if (websocketMessageType == this.websocketIntMessageType) {
      return parseInt(theMessage)
    } else if (websocketMessageType == this.websocketBoolMessageType) {
      return Boolean(theMessage)
    } else if (websocketMessageType == this.websocketStringMessageType) {
      return theMessage
    } else if (websocketMessageType == this.websocketJSONMessageType) {
      return JSON.parse(theMessage)
    } else {
      return null // invalid
    }
  }

  getWebsocketCustomEvent(websocketMessage) {
    if (websocketMessage.length < this.websocketMessagePrefixAndSepIdx) {
      return ""
    }
    const s = websocketMessage.substring(this.websocketMessagePrefixAndSepIdx, websocketMessage.length)
    const evt = s.substring(0, s.indexOf(this.websocketMessageSeparator))
    return evt
  }

  getCustomMessage(event, websocketMessage) {
    const eventIdx = websocketMessage.indexOf(event + this.websocketMessageSeparator)
    const s = websocketMessage.substring(eventIdx + event.length + this.websocketMessageSeparator.length + 2, websocketMessage.length)
    return s
  }

  messageReceivedFromConn(evt) {
    // console.log("messageReceivedFromConn")
    const that = this
    // check if qws message
    const message = evt.data
    if (message.includes(that.websocketMessagePrefix)) {
      const event_1 = that.getWebsocketCustomEvent(message)
      if (event_1 != "") {
        // it's a custom message
        that.fireMessage(event_1, that.getCustomMessage(event_1, message))
        return
      }
    }
    // console.log("fireNativeMessage")
    // it's a native websocket message
    that.fireNativeMessage(message)
  }

  OnConnect(fn) {
    if (this.isReady) {
      fn()
    }
    this.connectListeners.push(fn)
  }

  OnDisconnect(fn) {
    this.disconnectListeners.push(fn)
  }

  fireConnect() {
    for (let i = 0; i < this.connectListeners.length; i++) {
      this.connectListeners[i]()
    }
  }

  fireDisconnect() {
    for (let i = 0; i < this.disconnectListeners.length; i++) {
      this.disconnectListeners[i]()
    }
  }

  OnMessage(cb) {
    this.nativeMessageListeners.push(cb)
  }

  fireNativeMessage(websocketMessage) {
    for (let i = 0; i < this.nativeMessageListeners.length; i++) {
      this.nativeMessageListeners[i](websocketMessage)
    }
  }

  On(event, cb) {
    if (this.messageListeners[event] == null || this.messageListeners[event] == undefined) {
      this.messageListeners[event] = []
    }
    this.messageListeners[event].push(cb)
  }

  fireMessage(event, message) {
    const str = String(event)
    const event_final = str.substring(1, str.length)
    //      console.log(event_final, message);
    //    console.log(this.messageListeners);

    if (event_final === "ping") {
      return this.firePong()
    }

    if (this.messageListeners.hasOwnProperty(event_final)) {
      const cast = this.messageListeners[event_final]
      for (let i = 0; i < cast.length; i++) {
        //  console.log(cast);
        cast[i](message)
      }
      // }
    }
  }

  firePong() {
    this.Emit("pong", "")
  }

  Disconnect() {
    this.conn.close()
  }

  EmitMessage(websocketMessage) {
    this.conn.send(websocketMessage)
  }

  Emit(event, data) {
    const messageStr = this.encodeMessage(event, data)
    this.EmitMessage(messageStr)
  }
}
