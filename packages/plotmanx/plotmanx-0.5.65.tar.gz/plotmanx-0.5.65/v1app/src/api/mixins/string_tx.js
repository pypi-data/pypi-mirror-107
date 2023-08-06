// import EventBus from "vue-backgrounds";
import { LANUAGESMIX } from "@/i18n"
import { ___fromTrxToSun, ___fromSun2Floor, ___fromSun, toNumber } from "@/api/compress/bn"
import colorx from "@/api/mixins/mixin/colorx"
import { EventBus } from "vue-backgrounds"
import { getStoredItemStr } from "@/api/compress/urltool"

export default {
  mixins: [LANUAGESMIX, colorx],
  methods: {
    ChangeLanguage(lang = "") {
      if (lang === "") {
        if (this.$i18n.locale === "en") {
          this.$i18n.locale = "zh"
        } else {
          this.$i18n.locale = "en"
        }
      } else {
        this.$i18n.locale = lang
      }
      if (localStorage) {
        localStorage.setItem("lang", this.$i18n.locale)
      }
      const label = _.findLastIndex(this.languages, ["key", lang])
      this.notificationSuccess(`Changed Language to ${this.languages[label].label}`)
      EventBus.$emit("eventChangeLanguage", lang)
    },
    LanguageStart() {
      this.$i18n.locale = getStoredItemStr("lang", "en")
    },
    notificationError(msg) {
      let message_final
      if (msg === undefined) {
        message_final = "unknown error"
      } else if (typeof (msg) === "string") {
        message_final = msg
      } else if (typeof (msg) === "object" && msg.hasOwnProperty("message")) {
        message_final = msg.message
      } else {
        message_final = "unknown error"
      }
      this.$notice({
        type: "error", // alert, success, warning, error, info/information
        text: message_final
      })
    },
    notificationSuccess(msg) {
      this.$notice({
        type: "success", // alert, success, warning, error, info/information
        text: msg
      })
    },
    notificationWarning(msg) {
      this.$notice({
        type: "warning", // alert, success, warning, error, info/information
        text: msg
      })
    },
    notificationInfo(msg) {
      this.$notice({
        type: "info", // alert, success, warning, error, info/information
        text: msg
      })
    },
    notificationAlert(msg) {
      this.$notice({
        type: "alert", // alert, success, warning, error, info/information
        text: msg
      })
    },
    fromSun(anything) {
      return ___fromSun(anything)
    },
    toSun(anything) {
      return ___fromTrxToSun(anything)
    },
    bn2Number(anything) {
      return toNumber(anything)
    },
    status_display(m) {
      return "f-" + m
    },
    wallet_label(coin_name) {
      return "coin_" + String(coin_name).toLowerCase()
    },
    bankroll_label(coin_name) {
      return "bankroll_" + String(coin_name).toLowerCase()
    },
    betroll_label(coin_name) {
      return "betctrl_" + String(coin_name).toLowerCase()
    },
    dot_list_label(t) {
      return "dot_a_" + t.i
    },
    equal_assets(coin1, coin2) {
      return String(coin1).toLowerCase() === String(coin2).toLowerCase()
    },
    get_asset_display(amount, coin) {
      if (coin === "" || coin === undefined) {
        return "0.00 ---"
      } else {
        return Number(amount).toFixed(3) + " " + String(coin).toUpperCase()
      }
    }
  }
}
