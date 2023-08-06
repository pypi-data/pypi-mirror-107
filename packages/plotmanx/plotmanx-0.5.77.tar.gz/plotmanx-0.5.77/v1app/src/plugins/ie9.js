if (!window.cancelAnimationFrame) {
  window.cancelAnimationFrame = function (id) {
    clearTimeout(id)
  }
}
if (!window.requestAnimationFrame) {
  let lastTime = 0
  window.requestAnimationFrame = function (callback) {
    const currTime = new Date().getTime()
    const timeToCall = Math.max(0, 16.7 - (currTime - lastTime))
    const id = window.setTimeout(function () {
      // eslint-disable-next-line standard/no-callback-literal
      callback(currTime + timeToCall)
    }, timeToCall)
    lastTime = currTime + timeToCall
    return id
  }
}
if (window) {
// A manual UMD build of Fscreen: https://github.com/rafrex/fscreen
  (function (global) {
    "use strict"

    const key = {
      fullscreenEnabled: 0,
      fullscreenElement: 1,
      requestFullscreen: 2,
      exitFullscreen: 3,
      fullscreenchange: 4,
      fullscreenerror: 5
    }

    const webkit = ["webkitFullscreenEnabled", "webkitFullscreenElement", "webkitRequestFullscreen", "webkitExitFullscreen", "webkitfullscreenchange", "webkitfullscreenerror"]

    const moz = ["mozFullScreenEnabled", "mozFullScreenElement", "mozRequestFullScreen", "mozCancelFullScreen", "mozfullscreenchange", "mozfullscreenerror"]

    const ms = ["msFullscreenEnabled", "msFullscreenElement", "msRequestFullscreen", "msExitFullscreen", "MSFullscreenChange", "MSFullscreenError"]

    // so it doesn't throw if no window or document
    const doc = typeof window !== "undefined" && typeof window.document !== "undefined" ? window.document : {}

    // eslint-disable-next-line no-mixed-operators
    const vendor = "fullscreenEnabled" in doc && Object.keys(key) || webkit[0] in doc && webkit || moz[0] in doc && moz || ms[0] in doc && ms || []

    const fscreen = {
      requestFullscreen: function requestFullscreen(element) {
        return element[vendor[key.requestFullscreen]]()
      },
      requestFullscreenFunction: function requestFullscreenFunction(element) {
        return element[vendor[key.requestFullscreen]]
      },
      get exitFullscreen() {
        return doc[vendor[key.exitFullscreen]].bind(doc)
      },
      addEventListener: function addEventListener(type, handler, options) {
        return doc.addEventListener(vendor[key[type]], handler, options)
      },
      removeEventListener: function removeEventListener(type, handler) {
        return doc.removeEventListener(vendor[key[type]], handler)
      },
      get fullscreenEnabled() {
        return Boolean(doc[vendor[key.fullscreenEnabled]])
      },
      set fullscreenEnabled(val) {
      },
      get fullscreenElement() {
        return doc[vendor[key.fullscreenElement]]
      },
      set fullscreenElement(val) {
      },
      get onfullscreenchange() {
        return doc[("on" + vendor[key.fullscreenchange]).toLowerCase()]
      },
      set onfullscreenchange(handler) {
        doc[("on" + vendor[key.fullscreenchange]).toLowerCase()] = handler
      },
      get onfullscreenerror() {
        return doc[("on" + vendor[key.fullscreenerror]).toLowerCase()]
      },
      set onfullscreenerror(handler) {
        doc[("on" + vendor[key.fullscreenerror]).toLowerCase()] = handler
      }
    }
    global.fscreen = fscreen
  })(window)
}
