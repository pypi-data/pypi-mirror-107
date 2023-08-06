<template>
  <v-sheet height="90vh" class="text-center holo_sheet">
    <v-btn class="mt-6" text @click="$emit('close')">{{ $t("p_close") }}</v-btn>
    <v-card-text v-if="failed_payment" color="error" class="text-left">
      {{ failed_payment_message }}
    </v-card-text>
    <v-card-text v-else class="text-left">
      You will be making the amount ticket deposit.
    </v-card-text>
    <v-card-text class="text-center">
      <div class="pricebox uix ui statistics large center greenb">
        <div class="statistic">
          <div class="value">{{ bet_amoun | coinbalance_zero }}</div>
          <div class="label">TRX</div>
        </div>
      </div>
    </v-card-text>
    <!--<v-card-actions>
      <v-btn :disabled="control_button_disabled" depressed class="mt-6" rounded @click="plan_value">
        Plan
      </v-btn>
      <v-btn :disabled="control_button_disabled" depressed class="mt-6" rounded @click="clickPercent(0.25)">
        25%
      </v-btn>
      <v-btn :disabled="control_button_disabled" depressed class="mt-6" rounded @click="clickPercent(0.5)">
        50%
      </v-btn>
      <v-btn :disabled="control_button_disabled" depressed class="mt-6" rounded @click="clickPercent(0.75)">
        75%
      </v-btn>
      <v-btn :disabled="control_button_disabled" depressed class="mt-6" rounded @click="clickPercent(1.0)">
        100%
      </v-btn>
    </v-card-actions>-->
    <v-tabs fixed-tabs class="money-tabs">
      <v-tab :disabled="control_button_disabled" @click="clickPercent(0.25)">
        25%
      </v-tab>
      <v-tab :disabled="control_button_disabled" @click="clickPercent(0.50)">
        50%
      </v-tab>
      <v-tab :disabled="control_button_disabled" @click="clickPercent(0.85)">
        85%
      </v-tab>
      <v-tab :disabled="control_button_disabled" @click="clickPercent(1.00)">
        100%
      </v-tab>
    </v-tabs>
    <v-slider
      ref="slider_money" :disabled="control_button_disabled" v-model="slider_vault"
      step="1" height="100px" min="0" max="100"
      thumb-size="50" thumb-color="#bc5680" thumb-label
    ></v-slider>
    <v-card-actions>
      <v-btn :color="color_btn" :disabled="sign_disabled" :loading="payment_status === 2" class="mt-5" x-large depressed
             block @click="exexe_payment">
        <v-icon>mdi-data-matrix-edit</v-icon>
        {{ $t("bnt_confirm") }}
        <div slot="loader" class="text-center gradient-text-anim">
          Please wait ...
        </div>
      </v-btn>
    </v-card-actions>

  </v-sheet>
</template>

<script>

import { EventBus } from "vue-backgrounds"
import colorx from "@/api/mixins/mixin/colorx"
import { ___fromSun2Floor, ___fromTrxToSun } from "@/api/compress/bn"
import enterfund from "@/api/mixins/tron/enterfund"

/**
 * status:
 * 4 = normal
 * 3 = conditional check and cannot enter payment
 * 1 = conditional check and missing the upline code
 * 2 = payment progress
 */
export default {
  name: "Rdeposit",
  mixins: [colorx, enterfund],
  data() {
    return {
      debug_priceb: false,
      color_btn: "#5a4f35",
      color_txt: "#f1f1f1",
      payment_status: 4,
      slider_vault: 0,
      slider_label: "",
      bet_amoun: 0,
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
      return this.payment_status === 3 || this.payment_status === 1
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.check_status()
      this.onWatch("slider_vault")
      this.check_status()
    })
  },
  beforeDestroy() {
    this.unWatchAll()
  },
  methods: {
    /**
     * the long payment process
     * @returns {Promise<boolean>}
     */
    exexe_payment() {
      this.payment_status = 2
      const sun = ___fromTrxToSun(this.bet_amoun)
      this.enterfund_from_scale(sun)
    },
    check_status() {
      this.payment_status = 4
      if (isNaN(this.coin_trx_balance)) {
        this.failed_payment_message = "Sorry, you are currently not able to enter the fund. Wallet balance is not updated."
        this.payment_status = 3
      }

      if (this.coin_trx_balance < 50) {
        this.failed_payment_message = "Sorry, you need to have at least 50 TRX in your balance."
        this.payment_status = 1
      }

      if (this.debug_priceb) {
        this.payment_status = 4
      }
    },
    readyStatus() {
      this.check_status()
      this.bet_amoun = "0"
      this.setSliderVal(0)
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
      const actual = factor * parseInt(this.coin_trx_balance)
      this.bet_amoun = ___fromSun2Floor(actual)
    },
    update_from_slider(amount, previous) {
      this.mul(amount / 100)
    },
    clickPercent(fac) {
      this.mul(fac)
      this.setSliderVal(fac * 100)
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
      EventBus.$emit("debug_info", "payment", "trx", {
        id: "__"
      })
    }
  }
}
</script>
