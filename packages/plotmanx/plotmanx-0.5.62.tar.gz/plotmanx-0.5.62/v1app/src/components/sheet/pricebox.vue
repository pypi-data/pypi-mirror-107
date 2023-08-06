<template>
  <v-sheet height="90vh" class="text-center">
    <v-btn class="mt-6" text color="error" @click="$emit('close')">{{ $t("p_close") }}</v-btn>
    <v-card-text v-if="failed_payment" color="error" class="text-left">
      {{ failed_payment_message }}
    </v-card-text>
    <v-card-actions v-if="failed_payment" class="mt-5">
      <v-btn text color="#ff89b6" @click="go_back_find_referral">
        {{ $t("bnt_askcode") }}
      </v-btn>
    </v-card-actions>
    <v-card-text v-if="!failed_payment" class="text-left">
      Your referee code is <b>{{ local_upline_code }}</b>.
      According to the price tag, you will be granted as <b>{{ plan_title }}</b> by ..
    </v-card-text>
    <v-card-text class="text-center">
      <div class="ui statistics large center">
        <div class="statistic priceboxtag">
          <div class="value">{{ bet_amoun | coinbalance_zero }}</div>
          <div class="label">TRX</div>
        </div>
      </div>
    </v-card-text>
    <v-tabs fixed-tabs class="money-tabs">
      <v-tab :disabled="control_button_disabled" @click="plan_value">
        Plan
      </v-tab>
      <v-tab :disabled="control_button_disabled" @click="clickPercent(0.25)">
        25%
      </v-tab>
      <v-tab :disabled="control_button_disabled" @click="clickPercent(0.50)">
        50%
      </v-tab>
      <v-tab :disabled="control_button_disabled" @click="clickPercent(0.75)">
        75%
      </v-tab>
      <v-tab :disabled="control_button_disabled" @click="clickPercent(1.00)">
        100%
      </v-tab>
    </v-tabs>

    <!--   <v-card-actions class="mt-3">
      <v-btn :disabled="control_button_disabled" depressed rounded @click="plan_value">
        Plan
      </v-btn>
      <v-btn :disabled="control_button_disabled" depressed rounded @click="clickPercent(0.25)">
        25%
      </v-btn>
      <v-btn :disabled="control_button_disabled" depressed rounded @click="clickPercent(0.5)">
        50%
      </v-btn>
      <v-btn :disabled="control_button_disabled" depressed rounded @click="clickPercent(0.75)">
        75%
      </v-btn>
      <v-btn :disabled="control_button_disabled" depressed rounded @click="clickPercent(1.0)">
        100%
      </v-btn>
    </v-card-actions>-->
    <v-slider
      ref="slider_money" :disabled="control_button_disabled" v-model="slider_vault"
      step="1" height="100px" min="0" max="100"
      thumb-size="50" thumb-color="#bc5680" thumb-label
    ></v-slider>
    <v-card-actions class="mt-3">
      <v-btn :disabled="sign_disabled"
             :loading="payment_status === 2"
             x-large
             class="bigpaymentsign"
             block
             dark
             @click="payment">
        <v-icon>mdi-key-variant</v-icon>
        <!-- <v-icon>mdi-data-matrix-edit</v-icon>-->
        {{ $t("bnt_confirm") }}

        <template v-slot:loader>
          <span style="
                          align-items: center;
                          color: inherit;
                          display: flex;
                          flex: 1 0 auto;
                          justify-content: inherit;
                          line-height: normal;
                          position: relative;
              ">
            <v-icon>mdi-credit-card-wireless-outline</v-icon>  {{ $t("bnt_boardcast") }}
          </span>
        </template>

      </v-btn>
    </v-card-actions>
  </v-sheet>
</template>
<script>
import { EventBus } from "vue-backgrounds"
import { TRC975 } from "@/api/abi/trc975."
import price_plan from "@/api/mixins/tron/price_plan"
import { ___fromSun2Floor } from "@/api/compress/bn"
import main from "@/api/mixins/tron/main975"

/**
 * status:
 * 4 = normal
 * 3 = conditional check and cannot enter payment
 * 1 = conditional check and missing the upline code
 * 2 = payment progress
 */
export default {
  name: "PriceBoxEnter",
  mixins: [main, price_plan],
  data() {
    return {
      debug_priceb: false,
      color_txt: "#f1f1f1",
      //   local_upline_code: "----",
      payment_status: 4,
      slider_vault: 0,
      slider_label: "",
      bet_amoun: 0,
      bet_val_from_plan: 0,
      cooldown: 0,
      failed_payment_message: "--",
      watchers: {}
    }
  },
  computed: {
    control_button_disabled() {
      return this.payment_status === 2 || this.payment_status === 3 || this.payment_status === 1
    },
    failed_payment() {
      return this.payment_status === 3 || this.payment_status === 1
    },
    sign_disabled() {
      return (this.payment_status === 3 || this.payment_status === 1) || this.isTransactionInProcess
    },
    local_upline_code() {
      return this.$store.getters["forsage/show_upline"]
    },
    show_invitation_code() {
      return this.$store.getters["forsage/show_invitation_code"]
    },
    wallet_balance() {
      return this.$store.getters["wallet/QueryNowBalance"]
    },
    plan_title() {
      return "-"
      /* const r = this.eval_price_level(this.bet_amoun)
      if (r) {
        return r.title
      } else {
        return "-"
      } */
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.check_status()
      this.onWatch("slider_vault")
      // console.log("set wallet balance")
    })
  },
  beforeDestroy() {
    this.unWatchAll()
  },
  methods: {
    check_status() {
      this.payment_status = 4
      if (isNaN(this.wallet_balance)) {
        this.failed_payment_message = "Sorry, you are currently not able to enter the fund. Wallet balance is not updated."
        this.payment_status = 3
      }
      if (this.local_upline_code === "") {
        this.failed_payment_message = "Sorry, you are currently not able to enter the fund. You need to have the referral code first."
        this.payment_status = 1
      }
      if (this.wallet_balance < 50) {
        this.failed_payment_message = "Sorry, you need to have at least 50 TRX in your balance."
        this.payment_status = 1
      }
      if (this.debug_priceb) {
        this.payment_status = 4
      }
      // this.update_price_plan()
    },
    // public
    setBetAmount(n) {
      this.check_status()
      // const filtered_number = _.floor(n)
      const filtered_number = parseInt(n)
      this.bet_amoun = filtered_number
      this.bet_val_from_plan = filtered_number
      this.setSliderVal(filtered_number / this.fromSun(parseInt(this.wallet_balance)) * 100)
    },
    // public
    setSliderVal(anything) {
      if (typeof anything !== "number") {
        return
      }
      if (isNaN(anything)) {
        return
      }
      this.unWatchAll()
      this.slider_vault = _.floor(anything)
      this.onWatch("slider_vault")
    },
    onWatch(proper) {
      this.watchers[proper] = this.$watch(proper,
        (newVal, oldVal) => this.update_from_slider(newVal, oldVal)
      )
    },
    unWatchAll() {
      const watchers = Object.keys(this.watchers)
      watchers.forEach(name => this.watchers[name]())
    },
    mul(factor) {
      const actual = factor * parseInt(this.wallet_balance)
      this.bet_amoun = ___fromSun2Floor(actual)
    },
    update_from_slider(amount, previous) {
      this.mul(amount / 100)
    },
    clickPercent(fac) {
      this.mul(fac)
      this.setSliderVal(fac * 100)
    },
    plan_value(e) {
      e.preventDefault()
      this.bet_amoun = this.bet_val_from_plan
      const amount = parseInt(this.bet_val_from_plan) / this.fromSun(this.wallet_balance)
      this.setSliderVal(amount * 100)
    },
    go_back_find_referral() {
      EventBus.$emit("bottom_sheet_manual_enter")
    },

    /**
     * the long payment process
     * @returns {Promise<boolean>}
     */
    async payment() {
      this.payment_status = 2
      const invite = this.show_invitation_code
      const upline = this.local_upline_code
      const sun = this.toSun(this.bet_amoun)
      // console.log("sun value - ", sun)
      if (TRC975.Instance()) {
        try {
          this.commitBlockTransaction()
          const result = await TRC975.Instance().vegasRegular(invite, upline, sun)
          this.releaseBlockTransaction()
          if (!this.debug_priceb) {
            if (result) {
              this.payment_confirmed()
            } else {
              this.failed_payment_message = `The entered code ${code} is invalid.`
              this.payment_failed()
            }
          } else {
            this.payment_confirmed()
          }
        } catch (e) {
          console.error(e)
          this.releaseBlockTransaction()
          this.failed_payment_message = e.error
          this.payment_failed()
          EventBus.$emit("debug_info", "payment confirmed", "trx", e)
        }
      } else {
        this.failed_payment_message = "TRC975 instance is not found."
        console.error(this.failed_payment_message)
        this.payment_failed()
        EventBus.$emit("debug_info", "instance not found", "internal", {})
      }

      /*
      setTimeout(() => {
        this.payment_confirmed()
      }, 5000) */
    },
    payment_failed() {
      this.notificationError(this.failed_payment_message)
      setTimeout(() => {
        this.payment_status = 4
      }, 2000)
    },
    payment_confirmed() {
      this.notificationSuccess(this.$t("n_pmt_success"))
      this.payment_status = 4
      setTimeout(() => {
        this.$emit("close")
      }, 3000)
      EventBus.$emit("debug_info", "payment confirmed", "trx", {
        id: "__"
      })
    }
  }
}
</script>
