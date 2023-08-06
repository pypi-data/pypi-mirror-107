import string_tx from "@/api/mixins/string_tx"
import { EventBus } from "vue-backgrounds"
import { TRC975 } from "@/api/abi/trc975."
import { TRC757 } from "@/api/abi/trc757."

export default {
  mixins: [string_tx],
  data() {
    return {
      withdrawalloading: false,
      failed_payment_message: ""
    }
  },
  methods: {
    Check975Instance() {
      if (!TRC975.Instance()) {
        this.failed_payment_message = "TRC975 instance is not found."
        this.trx_failured()
        return true
      } else {
        return false
      }
    },
    Check757Instance() {
      if (!TRC757.Instance()) {
        this.failed_payment_message = "TRC757 instance is not found."
        console.error(this.failed_payment_message)
        this.trx_failured()
        return true
      } else {
        return false
      }
    },
    appendTransactionHistoryItem(msg, whatsort, dat) {
      this.$store.dispatch("wallet/newEventTransaction", {
        msg,
        whatsort,
        dat
      })
    },
    trx_failured() {
      this.withdrawalloading = false
      this.notificationError(this.failed_payment_message)
      this.appendTransactionHistoryItem("payment", "trx", this.failed_payment_message)
    },
    straightInto(pid) {
      this.$router.push(pid)
    },
    gotoHome() {
      this.$router.push("/")
      this.notificationAlert("this contract requires network nile")
    },
    open_sheet_about(e) {
      e.preventDefault()
      EventBus.$emit("bottom_sheet_about")
    },
    open_sheet_referral(e) {
      e.preventDefault()
      EventBus.$emit("bottom_sheet_manual_enter")
    },
    open_sheet_console(e) {
      e.preventDefault()
      EventBus.$emit("bottom_sheet_debug")
    },
    switch_account(e) {
      e.preventDefault()
      EventBus.$emit("switch_account")
    },
    /**
     * make deposit for roulette machine
     * @param amount
     * @returns {Promise<void>}
     */
    async makedepositforroulette(amount) {
      if (this.Check757Instance()) {
        return
      }
      this.debugTronLink(true)
      try {
        const result = await TRC757.Instance().depositFundsTrx(amount)
        if (result) {
          this.notificationSuccess("Deposit success!\nBlock confirmed.")
        } else {
          this.failed_payment_message = "Fail to deposit"
          this.trx_failured()
        }
      } catch (e) {
        this.failed_payment_message = e.toString()
        this.trx_failured()
      }
      this.debugTronLink(false)
    },
    async machine757takeout() {
      if (this.Check757Instance()) {
        return
      }
      try {
        const result = await TRC757.Instance().withdrawFundsTrx()
        if (result) {
          this.notificationSuccess("Withdrawal success!\nBlock confirmed.")
        } else {
          this.failed_payment_message = "Fail to deposit"
          this.trx_failured()
        }
      } catch (e) {
        this.failed_payment_message = e.toString()
        this.trx_failured()
      }
    },
    /**
     * Contract related operations with independent instance
     *
     * @returns {Promise<void>}
     */
    async reinvestment() {
      if (this.Check975Instance()) {
        return
      }
      try {
        const result = await TRC975.Instance().reinvestment()
        if (result) {
          this.notificationSuccess("Reinvest success!\nBlock confirmed.")
        } else {
          this.failed_payment_message = "Fail to reinvest"
          this.trx_failured()
        }
      } catch (e) {
        this.failed_payment_message = e.toString()
        this.trx_failured()
      }
    },
    /**
     * Contract related operations with independent instance
     * @param _a, _b, amount_sun
     * @returns {Promise<void>}
     */
    async investNew(_a, _b, amount_sun) {
      if (this.Check975Instance()) {
        return
      }
      try {
        await TRC975.Instance().vegas(_a, _b, amount_sun)
        this.notificationSuccess("New Success\nBlock confirmed.")
      } catch (e) {
        if (typeof e === "string") {
          this.failed_payment_message = `${e.toString()} with amount ${amount_sun}, invite ${_a}, refer ${_b}`
        } else {
          this.failed_payment_message = `${JSON.stringify(e)} with amount ${amount_sun}, invite ${_a}, refer ${_b}`
        }
        this.trx_failured()
      }
    }
  }
}
