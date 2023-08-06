import { TRC757 } from "@/api/abi/trc757."
import walletx from "@/api/mixins/tron/walletx"
import string_tx from "@/api/mixins/string_tx"

export default {
  mixins: [walletx, string_tx],
  methods: {
    async sphere_update() {
      if (this.Check757Instance()) {
        return
      }
      const dat = await TRC757.Instance().sphere_x()
      if (this.isDebug()) {
        console.group("shenzhen data ==> ")
        console.log(dat)
        console.groupEnd()
      }
      await this.$store.dispatch("roulette/shenzhen", dat)
    },
    trx_failured() {
      this.withdrawalloading = false
      this.notificationError(this.failed_payment_message)
      this.appendTransactionHistoryItem("payment", "trx", this.failed_payment_message)
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
    /**
     * make deposit for roulette machine
     * @param amount
     * @returns {Promise<void>}
     */
    async enterfund_from_scale(amount) {
      const _that = this
      if (this.Check757Instance()) {
        return
      }
      const depositfunc = {
        signer(payload) {
          _that.report_event(payload)
          _that.notificationInfo(`Sign deposit ${payload.uuid}`)
          return true
        },
        reply(payload) {
          _that.notificationInfo(`The broadcast transaction uuid ${payload.data.txID}`)
          _that.$emit("close")
          setTimeout(_that.sphere_update, 6000)
          return true
        }
      }

      _that.tronLink.setCallbackFunctionCall("depositFundsTrx()", depositfunc)

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
    }
  }
}
