<template>
  <v-card>
    <v-card-text align="left">
      Pocket / Staked {{ pocket_fund | trx }} TRX / {{ locked_fund | trx }}TRX<br/>
      Last Result: {{ gg_result }} <br/>
      Block: {{ gg_block }} <br/>
      Bank roll / Insured {{ banker_fund | trx }} TRX/ {{ banker_locked_fund | trx }}TRX<br/>
      Liquidity {{ management_fund | trx }}TRX
    </v-card-text>
    <reellet ref="scale_reel" :debug_ds="false" @reel_roll_state_rolling="roll_start" @reel_roll_complete="roll_done"/>
    <v-row justify="space-around" style="margin: 0">
      <v-tabs fixed-tabs class="money-tabs">
        <v-tab :disabled="loading|| ui_disabled" @click="clickPercent(0.25)">
          25%
        </v-tab>
        <v-tab :disabled="loading|| ui_disabled" @click="clickPercent(0.50)">
          50%
        </v-tab>
        <v-tab :disabled="loading|| ui_disabled" @click="clickPercent(0.75)">
          75%
        </v-tab>
        <v-tab :disabled="loading|| ui_disabled" @click="clickPercent(1.00)">
          100%
        </v-tab>
      </v-tabs>
    </v-row>
    <v-row justify="space-around" style="margin: 0">
      <v-col>
        <v-slider
          ref="slider_money" :disabled="loading|| ui_disabled" v-model="slider_vault"
          step="1" height="100px" min="0" max="100"
          thumb-size="50" thumb-color="#bc5680" thumb-label
        ></v-slider>
      </v-col>
    </v-row>
    <v-row style="margin: 0">
      <v-col>
        <v-badge
          :content="state_msg"
          :value="state_msg"
          :color="c5_primary"
          overlap>
          <v-btn :disabled="loading||bet_button_disabled" class="mt-6" text @click="started_roll">
            {{ bet_button_label }}
          </v-btn>
        </v-badge>
      </v-col>
      <v-col>
        <div class="ui statistics center tiny">
          <div class="statistic">
            <div class="value">{{ bet_amount_for_roulette_pv | coinbalance_zero }}</div>
            <div class="label">TRX</div>
          </div>
        </div>
      </v-col>
    </v-row>
    <v-card-actions v-if="isDebug()">
      <v-btn :disabled="loading" class="mt-6" text @click="$refs.scale_reel.roll_start()">
        Start
      </v-btn>
      <v-btn :disabled="loading" class="mt-6" text @click="$refs.scale_reel.stop_debug()">
        Stop
      </v-btn>
    </v-card-actions>
    <v-card-actions>
      <v-btn :disabled="loading" class="mt-6" text @click="open_sheet_deposit_game">
        <v-icon>mdi-clock-time-nine-outline</v-icon>
        Deposit Fund
      </v-btn>
      <v-btn :disabled="loading||cash_out_button_disable" class="mt-6" text @click="machine757takeout">
        <v-icon>mdi-clock-time-nine-outline</v-icon>
        Cash Out
      </v-btn>
    </v-card-actions>
  </v-card>
</template>
<script>
import roulette from "@/api/mixins/tron/main757"
import { EventBus } from "vue-backgrounds"
import { TRC757 } from "@/api/abi/trc757."
import nav from "@/api/mixins/tron/nav"
import Reellet from "@/components/roulettec757/reellet"
import { ___fromSun2Floor } from "@/api/compress/bn"

export default {
  name: "VCardRoulette",
  components: { Reellet },
  mixins: [roulette, nav],
  data() {
    return {
      state_msg: "",
      slider_vault: 0,
      watchers: {},
      loading: true
    }
  },
  mounted() {
    this.LanguageStart()
    this.$nextTick(() => {
      this.onWatch("slider_vault")
    })
  },
  beforeDestroy() {
  },
  methods: {
    loadingSet(b) {
      this.loading = b
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
      this.watchers[proper] = this.$watch(proper, (newVal, oldVal) => this.update_from_slider(newVal, oldVal))
    },
    unWatchAll() {
      const watchers = Object.keys(this.watchers)
      watchers.forEach(name => this.watchers[name]())
    },
    mul(factor) {
      const actual = factor * parseInt(this.max_bet)
      this.bet_amount_for_roulette_pv = ___fromSun2Floor(actual)
    },
    update_from_slider(amount, previous) {
      this.mul(amount / 100)
    },
    clickPercent(fac) {
      this.mul(fac)
      this.setSliderVal(fac * 100)
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
    open_sheet_deposit_game(e) {
      e.preventDefault()
      EventBus.$emit("bottom_deposit_game")
    }
  }
}
</script>
<style lang="scss">

</style>
