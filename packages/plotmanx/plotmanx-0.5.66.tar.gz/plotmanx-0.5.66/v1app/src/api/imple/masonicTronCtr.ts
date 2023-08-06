// @ts-ignore
import { EventBus } from "vue-backgrounds"

export class MController {
    heartbeat: number;
    heartbeatrate: number = 5000;
    callback_heartbeat: Function;
    tronWebInstance: any;

    constructor() {
      if (!this.heartbeat) {
        // @ts-ignore
        this.heartbeat = setInterval(() => {
          EventBus.$emit("heartbeat")
          if (this.callback_heartbeat) {
            this.callback_heartbeat()
          }
          this.detectTronWeb()
        }, this.heartbeatrate)
        EventBus.$emit("heartbeat")
      }
      EventBus.$on("hb-save-battery", () => {
        this.heartbeatrate = 20000
      })
      EventBus.$on("hb-high-precision", () => {
        this.heartbeatrate = 2000
      })
      EventBus.$on("hb-normal", () => {
        this.heartbeatrate = 9000
      })
      EventBus.$on("hb-custom", (musecond) => {
        if (typeof musecond === "number") {
          this.heartbeatrate = musecond
        }
      })
      if (window && !window.hasOwnProperty("__TronController__")) {
        // @ts-ignore
        window.__TronController__ = this
      }
      this.detectTronWeb()
    }

    setHbCustom(n: number): MController {
      this.heartbeatrate = n
      return this
    }

    setHbHightF(): MController {
      this.heartbeatrate = 2000
      return this
    }

    setHbNormal(): MController {
      this.heartbeatrate = 9000
      return this
    }

    setHbBatteryWise(): MController {
      this.heartbeatrate = 20000
      return this
    }

    heart_beat(callback) : MController {
      this.callback_heartbeat = callback
      return this
    }

    getTronWeb(): any {
      return this.tronWebInstance
    }

    private detectTronWeb() {
      if (window && window.hasOwnProperty("tronWeb") && !this.tronWebInstance) {
        // @ts-ignore
        this.tronWebInstance = window.tronWeb
      }
    }

    public static Instance(): (MController | any | boolean) {
      if (window && window.hasOwnProperty("__TronController__")) {
        // @ts-ignore
        const obj = window.__TronController__
        if (obj instanceof MController) {
          return (obj) as MController
        } else {
          return (obj) as MController
        }
      } else {
        return new MController()
      }
    }
}
