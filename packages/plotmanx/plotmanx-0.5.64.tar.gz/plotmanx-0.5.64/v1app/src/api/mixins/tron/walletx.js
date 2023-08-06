import { TronLinkComponent, ImTokenComponent, TronLink } from "vue-tronlink"
import { Base64 } from "@/api/compress/base64"
import { EventBus } from "vue-backgrounds"

export default {
  mixins: [TronLinkComponent, ImTokenComponent],
  computed: {
    coin_symbol() {
      return this.$store.getters["wallet/QueryNowSymbol"]
    },
    contractAddress() {
      return this.$store.getters["wallet/addressContract"]
    },
    mywalletaddress() {
      return this.$store.getters["wallet/user_account"]
    },
    contractBalance() {
      return this.$store.getters["wallet/QueryContractBalance"]
    },
    coin_trx_balance() {
      return this.$store.getters["wallet/QueryNowBalance"]
    }
  },
  data() {
    return {
      contractInstance: "",
      tronClient: false,
      tronUtils: false,
      tronTrx: false,
      txObject: {},
      basicOptions: {},
      networkName: "",
      txs: [],
      txHashToIndex: [],
      token_send_approval_hash: "",
      _debug: true,
      _scan_error: false,
      _worker_process: false,
      _loading_content: ""
    }
  },
  methods: {
    wallet_scan() {
      this.loading_message("read wallet data")
      this.tronLink.getCoinTRX((x) => {
        this.saveLocal("wallet/save_balance", x)
      }, (e) => {
        this.report_error(e)
      })
    },
    checkIsEnough(amount_sun) {
      const wallet_sun = this.coin_trx_balance
      return wallet_sun > amount_sun
    },
    apWallHist(msg, whatsort, dat) {
      if (this.$store) {
        this.$store.dispatch("wallet/newEventTransaction", {
          msg,
          whatsort,
          dat
        })
      }
    },
    /**
     * trigger when the scan has error
     * @param e
     */
    report_scan_error(e) {
      this._scan_error = true
      this.apWallHist("scan wallet", "read", `error in scanning ${e.toString()}`)
    },
    /**
     * keep the heart beat checker
     * @returns {boolean}
     */
    keep_hb() {
      return this._scan_error || this._worker_process || !this.tronLink || !this.tronWeb
    },
    /**
     * Generate
     * only upper case letters
     * @returns {*}
     * @constructor
     */
    InviteCodeGenerator() {
      const registered = this.$store.getters["forsage/registered_user"]
      if (registered) {
        return
      } else {
        return
      }
      this.loading_message("gen user code")
      const address = this.tronLink.getAccountAddress()
      const check = this.tronWeb.toHex(address)
      const pubKey = this.tronWeb.utils.ethersUtils.keccak256(check)
      const b64 = new Base64()
      const base64 = b64.encode(pubKey)
      const onlyLetters = base64.match(/[a-zA-Z]+/g).join("").toUpperCase()
      const onlyUniqueLetters5 = onlyLetters.split("").filter((item, i, ar) => ar.indexOf(item) === i).join("").substring(0, 5)
      this.apWallHist("generate", "UI", `Should generate code for :${registered} and the default code is gen ${onlyUniqueLetters5}`)
      this.$store.dispatch("forsage/gen_code", onlyUniqueLetters5)
    },
    isDebug() {
      return this._debug
    },
    getVal(val, debug, format = "") {
      if (debug) {
        return "8,880,000"
      } else {
        return this.loadLocal(val)
      }
    },
    getBool(key, debug) {
      if (this.$store) {
        // eslint-disable-next-line no-unused-expressions
        return !!this.$store.getters[key]
      } else {
        return false
      }
    },
    loadLocal(key) {
      if (this.$store) {
        // eslint-disable-next-line no-unused-expressions
        return this.$store.getters[key]
      }
    },
    saveLocal(key, content) {
      if (this.$store) {
        this.$store.dispatch(key, content)
      }
    },
    report_error(e) {
      this.apWallHist("error", "internal", e)
    },
    report_event(e) {
      this.apWallHist("event", "trx", e)
    },
    report_error_trn(e, event) {
      this.apWallHist("error", event, e)
    },
    report_debug(eobject) {
      this.apWallHist("i", "debug", eobject)
    },
    event_loading_process(sw) {
      this._worker_process = sw
      EventBus.$emit("workprocess", sw)
      if (!sw) {
        this._loading_content = ""
      }
    },
    event_loading_content(content_detail) {
      this._loading_content = content_detail
      EventBus.$emit("loading_progress_content", content_detail)
    },
    debug(bool) {
      this._debug = bool
    },
    loading_message(payload) {
      EventBus.$emit("loading-message", payload)
    }
  }
}
