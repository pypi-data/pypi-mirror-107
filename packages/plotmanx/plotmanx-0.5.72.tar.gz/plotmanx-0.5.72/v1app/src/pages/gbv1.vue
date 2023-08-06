<template>
  <v-main class="welcome_bacground_xxx">
    <loaddisc
      :show="loading"
      :show-loading-text="true"
      disc-type="black"/>

    <v-container fill-height fluid>
      <v-layout column>
        <roulette-v-card ref="gamble_roulette"/>

        <v-card class="mt-3 mb-3 mt-sm-6 mb-sm-6 mx-lg-auto">
          <v-card-text class="text-left">
            The card split can be played as 1:1 bet
          </v-card-text>
          <v-card-actions>
            <v-btn ref="langSelect" depressed color="transparent" @click.stop="open_lang_selection">
              Languages
            </v-btn>
            <v-btn depressed color="transparent" @click="open_sheet_about">
              About
            </v-btn>
            <v-btn depressed color="transparent" @click="open_sheet_console">
              Console
            </v-btn>
            <v-menu
              v-if="menuLang"
              ref="setting_languages"
              :activator="$refs.langSelect.$el"
              :value="true"
              transition="slide-x-transition"
              tile
              offset-y>

              <v-list elevation="10">
                <v-list-item v-for="(val, k) in languages" :key="k" @click="onItemClicked(val)">
                  <v-list-item-title align="left">{{ val.label }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </v-card-actions>
        </v-card>

      </v-layout>
    </v-container>
  </v-main>
</template>

<script>

import RouletteVCard from "@/components/roulettec757/VCardRoulette"
import Loaddisc from "@/components/util/loaddisc"
import Referralpad from "@/components/sheet/referralpad"
import Cardgen from "@/components/cardgen/codegen"
import roulette from "@/api/mixins/tron/main757"
import { EventBus } from "vue-backgrounds"
import { getURLReferralCode } from "@/api/compress/urltool"

export default {
  layout: "bottom",
  components: {
    RouletteVCard,
    Loaddisc,
    Referralpad,
    Cardgen
  },
  mixins: [roulette],
  data() {
    return {
      loading: true,
      withdrawalloading: false,
      failed_payment_message: "",
      my_invitation_code: "",
      menuLang: false
    }
  },
  created() {
    this.$on("notify_tron_installed", this.installed)
    EventBus.$on("heartbeat", this.beat)
  },
  beforeDestroy() {
    this.$off("notify_tron_installed", this.installed)
    EventBus.$off("heartbeat", this.beat)
  },
  mounted() {
    this.$nextTick(() => {
      this.LanguageStart()
      this.beat()
      this.debug(false)
      this.$on("notify_tron_account_set", async (name, address) => {
        await this.game_system_scan()
      })
      this.$on("notify_tron_not_install", () => {
      })
      this.$on("notify_tron_node_change", () => {
        if (!this.confirmDappChainID(process.env.network)) {
          this.gotoHome()
          this.notificationWarning(`the current network is not on ${process.env.network}.`)
        }
      })
    })
  },
  methods: {
    // event
    installed() {
      this.$refs.gamble_roulette.loadingSet(true)
      this.contract_roulette_init(() => {
        this.wallet_scan()
        getURLReferralCode()
        if (this.loading) {
          this.loading = false
        }
        this.$refs.gamble_roulette.loadingSet(false)
      })
    },
    // event
    async beat() {
      if (this.keep_hb()) {
        return
      }
      try {
        this.wallet_scan()
        await this.game_system_scan()
      } catch (e) {
        this.report_scan_error(e)
      }
    },
    /**
     * language setting in here
     */
    open_lang_selection() {
      if (this.menuLang && !this.$refs.setting_languages.isContentActive) {
        return
      }
      if (!this.menuLang) {
        this.menuLang = !this.menuLang
        if (this.menuLang) {
          this.$nextTick(() => this.$refs.setting_languages.activate())
        }
      }
    },
    onItemClicked(evt) {
      this.menuLang = false
      if (!this.menuLang) {
        // this.$nextTick(() => this.$refs.setting_languages.deactivate())
        this.ChangeLanguage(evt.key)
      }
    }
  }

}
</script>

<style scoped>

</style>
