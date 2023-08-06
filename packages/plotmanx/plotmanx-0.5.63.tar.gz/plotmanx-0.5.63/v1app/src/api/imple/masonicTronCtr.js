import { EventBus } from "vue-backgrounds";
export class MController {
    constructor() {
        this.heartbeatrate = 5000;
        if (!this.heartbeat) {
            this.heartbeat = setInterval(() => {
                EventBus.$emit("heartbeat");
                if (this.callback_heartbeat) {
                    this.callback_heartbeat();
                }
                this.detectTronWeb();
            }, this.heartbeatrate);
            EventBus.$emit("heartbeat");
        }
        EventBus.$on("hb-save-battery", () => {
            this.heartbeatrate = 20000;
        });
        EventBus.$on("hb-high-precision", () => {
            this.heartbeatrate = 2000;
        });
        EventBus.$on("hb-normal", () => {
            this.heartbeatrate = 9000;
        });
        EventBus.$on("hb-custom", (musecond) => {
            if (typeof musecond === "number") {
                this.heartbeatrate = musecond;
            }
        });
        if (window && !window.hasOwnProperty("__TronController__")) {
            window.__TronController__ = this;
        }
        this.detectTronWeb();
    }
    setHbCustom(n) {
        this.heartbeatrate = n;
        return this;
    }
    setHbHightF() {
        this.heartbeatrate = 2000;
        return this;
    }
    setHbNormal() {
        this.heartbeatrate = 9000;
        return this;
    }
    setHbBatteryWise() {
        this.heartbeatrate = 20000;
        return this;
    }
    heart_beat(callback) {
        this.callback_heartbeat = callback;
        return this;
    }
    getTronWeb() {
        return this.tronWebInstance;
    }
    detectTronWeb() {
        if (window && window.hasOwnProperty("tronWeb") && !this.tronWebInstance) {
            this.tronWebInstance = window.tronWeb;
        }
    }
    static Instance() {
        if (window && window.hasOwnProperty("__TronController__")) {
            const obj = window.__TronController__;
            if (obj instanceof MController) {
                return (obj);
            }
            else {
                return (obj);
            }
        }
        else {
            return new MController();
        }
    }
}
