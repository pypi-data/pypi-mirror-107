<template>
  <v-app>
    <nuxt/>
    <v-footer absolute padless>
      <v-bottom-navigation v-model="bottomNav" shift dark>
        <v-btn
          v-for="(item, i) in items"
          :to="item.to" :key="i" :value="item.key" nuxt>
          <span style="alignment: center; display: inline-table">{{ $t(item.title) }}</span>
          <v-icon>{{ item.icon }}</v-icon>
        </v-btn>
      </v-bottom-navigation>
    </v-footer>
    <v-bottom-sheet v-model="sheet_4" :retain-focus="false" inset persistent>
      <p-debug ref="debug_console" @close="sheet_4=false"/>
    </v-bottom-sheet>
    <v-bottom-sheet v-model="sheet_1" inset persistent>
      <div class="versace_backdrop_container">
        <div class="pattern_layer"></div>
        <div class="versace_dark"></div>
      </div>
      <referralpad ref="pinbox_section" :coded="query_code" @close="sheet_1=false"/>
    </v-bottom-sheet>
    <v-bottom-sheet v-model="sheet_2" inset persistent>
      <price-box-enter ref="price_box" @close="sheet_2=false"/>
    </v-bottom-sheet>
    <v-bottom-sheet v-model="sheet_5" inset persistent>
      <div class="versace_backdrop_container">
        <div class="pattern_layer"></div>
        <div class="versace_light"></div>
      </div>
      <rdeposit ref="deposit_roulette_box" @close="sheet_5=false"/>
    </v-bottom-sheet>
    <v-bottom-sheet v-model="sheet_3" :retain-focus="false" inset persistent>
      <v-sheet class="text-center" height="90vh">
        <v-btn class="mt-6" text color="error" @click="sheet_3=false">{{ $t("p_close") }}</v-btn>
        <terms/>
      </v-sheet>
    </v-bottom-sheet>
  </v-app>
</template>

<script>
import { EventBus } from "vue-backgrounds"
import Referralpad from "@/components/sheet/referralpad"
import PriceBoxEnter from "@/components/sheet/pricebox"
import nav from "@/api/mixins/tron/nav"
import { MController } from "@/api/imple/masonicTronCtr"
import terms from "@/components/sheet/terms"
import string_tx from "@/api/mixins/string_tx"
import PDebug from "@/components/sheet/debug"
import Rdeposit from "@/components/sheet/rdeposit"

export default {
  components: {
    Rdeposit,
    PDebug,
    terms,
    PriceBoxEnter,
    Referralpad
  },
  mixins: [nav, string_tx],
  data() {
    return {
      heartbeat: false,
      heartbeatrate: 9000,
      bottomNav: "home",
      sheet_1: false,
      sheet_2: false,
      sheet_3: false,
      sheet_4: false,
      sheet_5: false,
      query_code: "",
      items: [
        {
          icon: "mdi-sail-boat",
          title: "bnt_welcome",
          key: "home",
          to: "/main"
        },
        {
          icon: "mdi-qrcode",
          title: "bnt_share",
          key: "qr",
          to: "/qr"
        },

        {
          icon: "mdi-bank",
          title: "bnt_price_plan",
          key: "priceplan",
          to: "/gbv1"
        }
        /**
         *
         {
          icon: "mdi-bank",
          title: "bnt_price_plan",
          key: "priceplan",
          to: "/levels"
        }
         */
      ]
    }
  },
  mounted() {
    this.$nextTick(() => {
      MController.Instance().setHbCustom(10000)
      EventBus.$on("bottom_sheet_refer", (enter_code) => {
        if (enter_code.match(/^[a-zA-Z]{5}$/)) {
          this.sheet_1 = true
          this.query_code = enter_code
        } else {
          console.log("entered code is invalid:", enter_code)
        }
      })
      /**
       * display the sheet for entering referral code
       */
      EventBus.$on("bottom_sheet_manual_enter", () => {
        this.sheet_off()
        this.sheet_1 = true
      })
      /**
       *
       */
      EventBus.$on("bottom_sheet_about", () => {
        this.sheet_off()
        this.sheet_3 = true
      })

      EventBus.$on("bottom_sheet_debug", () => {
        this.sheet_off()
        this.sheet_4 = true
      })

      /**
       * check price plan
       */
      EventBus.$on("check_price_plan_action", () => {
        this.sheet_off()
        this.straightInto("levels")
        this.bottomNav = "priceplan"
      })
      /**
       * contract specific actions
       */
      EventBus.$on("price_plan_enter_deal", (key, amount) => {
        this.sheet_off()
        this.sheet_2 = true
        setTimeout(() => {
          const price = this.$refs.price_box
          // console.log("enter price box price", price)
          price.setBetAmount(amount)
        }, 500)
      })

      EventBus.$on("bottom_deposit_game", () => {
        this.sheet_off()
        this.sheet_5 = true
        setTimeout(() => {
          const stakingboxed = this.$refs.deposit_roulette_box
          stakingboxed.readyStatus()
        }, 500)
      })

      EventBus.$on("debug_info", this.appendItem)
    })
  },
  methods: {
    sheet_off() {
      this.sheet_2 = false
      this.sheet_1 = false
      this.sheet_3 = false
      this.sheet_4 = false
    },
    appendItem(msg, whatsort, dat) {
      this.$store.dispatch("wallet/newEventTransaction", {
        msg,
        whatsort,
        dat
      })
    }
  }
}
</script>
<style scoped lang="scss">
html {
  font-family: "Source Sans Pro", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  font-size: 16px;
  word-spacing: 1px;
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  box-sizing: border-box;
}

*, *:before, *:after {
  box-sizing: border-box;
  margin: 0;
}

.base_maze {
  z-index: -1;
}
</style>
