<template>
  <v-main class="welcome_bacground_xxx">
    <loaddisc
      :show="loading"
      :show-loading-text="true"
      loading-text="Contacting the tron network..."
      disc-type="black"/>

    <v-container fill-height fluid>
      <v-layout column>
        <v-flex ref="scroll" class="main-container">
          <div class="ui statistics horizontal tiny">
            <div class="statistic olive" in-group="brief">
              <div class="value">{{ sum_investors | unit }}</div>
              <div class="label">{{ $t("p_all_accs") }}</div>
            </div>
            <div class="statistic olive" in-group="brief">
              <div class="value">{{ bank_fund }}</div>
              <div class="label">{{ $t("p_total_income") }}</div>
            </div>
          </div>

          <v-card
            :color="c3_primary"
            class="mb-3 mt-sm-6 mb-sm-6 mx-lg-auto"
            dark
            rounded
            elevation="12">

            <v-card-title>
              <v-icon>mdi-chart-areaspline</v-icon>
              My Pocket
            </v-card-title>
            <v-card-text v-if="!userRegistered" class="text-left">
              Please register by getting the referral code from your business partner. {{ $t("msg_stay_tuned") }}
            </v-card-text>
            <v-card-text v-if="userRegistered">
              <div class="ui statistics horizontal mini">
                <div class="statistic olive" in-group="subam">
                  <div class="value">{{ wallet_coin |trx }}</div>
                  <div class="label">TRX Wallet {{ $t("bnt_balance") }}</div>
                </div>
              </div>
            </v-card-text>
            <v-card-actions>
              <v-btn v-if="!userRegistered" depressed color="transparent" @click="open_sheet_referral">
                {{ $t("bnt_invcode") }}
              </v-btn>
            </v-card-actions>
            <cardgen ref="cardg" :code="my_invitation_code"/>
          </v-card>
          <v-card>
            <mine-field
              ref="mine-pick"
              :box-length="50"
              :lvl1h="5"
              :lvl1m="4"
              :lvl1w="8"
              :max-picked="10"
              class="center mt-6"
              @update_list="setlist"
            />
            <v-row>
              <v-col v-for="(a,b) in factors" :key="b">
                <span>{{ b }} hits</span>
                <span>{{ a }}</span>
              </v-col>
            </v-row>

            <v-card-actions class="mt-6">
              <v-btn :disabled="factors.length ===0 || cannot_purchase" depressed color="transparent"
                     @click="open_sheet_referral">
                BUY TICKET
              </v-btn>

              <v-btn :disabled="cannot_draw" depressed color="transparent"
                     @click="snap_draw">
                SNAP DRAW
              </v-btn>
            </v-card-actions>
            <v-card-text>
              <p>{{ round_number | unit }} Round</p>
              <p>{{ ticket_no | unit }} Ticket No</p>
              <p>{{ remain_time | unixduration }} Remain Time</p>
            </v-card-text>
            <cardgen ref="cardg" :code="my_invitation_code"/>
          </v-card>
          <v-card class="mt-3 mb-3 mt-sm-6 mb-sm-6 mx-lg-auto">
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

        </v-flex>
      </v-layout>
    </v-container>
  </v-main>
</template>
<script>

import { EventBus } from "vue-backgrounds"
import Loaddisc from "@/components/util/loaddisc"
import nav from "@/api/mixins/tron/nav"
import Referralpad from "@/components/sheet/referralpad"
import Cardgen from "@/components/cardgen/codegen"
import { MineField } from "vue-minefield"
import { getURLReferralCode } from "@/api/compress/urltool"
import main773 from "@/api/mixins/tron/main773"

export default {
  layout: "bottom",
  components: {
    MineField,
    Loaddisc,
    Referralpad,
    Cardgen
  },
  mixins: [nav, main773],
  data() {
    return {
      loading: true,
      withdrawalloading: false,
      failed_payment_message: "",
      my_invitation_code: "",
      menuLang: false
    }
  },
  watch: {
    cannot_purchase(val) {
      const el = this.$refs["mine-pick"]
      el.setDisabled(val)
      el.setChildrenLocked(val)
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
        await this.findPlayerStatus()
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
      this.contract_init().then(() => {
        this.wallet_scan()
        getURLReferralCode()
        this.InviteCodeGenerator()
        this.contract_scan()
        if (this.loading) {
          this.loading = false
        }
      })
    },
    // event
    async beat() {
      if (this.keep_hb()) {
        return
      }
      try {
        this.wallet_scan()
        await this.contract_scan(() => {
          this.gotoHome()
        })
      } catch (e) {
        this.report_scan_error(e)
      }
    },
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
<style lang="scss">
@import "node_modules/_vue-minefield@0.3.75@vue-minefield/src/presents/base";

.field_mfx_wrapper.center {
  display: inline-flex;
}

.box_nfx {
  margin: 1px;
  border: 1px solid #222;
  @include btn3dbase;
  @include btn3dGreen;

  span {
    font-size: 14px;
    color: #ffffff;
    align-self: center;
    justify-self: center;
    width: 100%;
  }

  &.highlight {
    @include claw_machine_button_style_ex1(#73ff4a);
    @include activeButton;

    span {
      color: #c61616;
    }
  }

  &.reward {
    background-color: #73ff4a;
  }

}

</style>
