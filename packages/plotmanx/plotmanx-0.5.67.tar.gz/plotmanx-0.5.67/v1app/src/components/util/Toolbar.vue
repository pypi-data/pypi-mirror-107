<template>
  <section class="toolbar container-fluid icy">
    <div class="toolbar_flex">
      <div class="small_bar">
        <div class="small_box">
          <span class="username_f">{{ user_id }}</span>
          <span class="moneybank_f">{{ currency }} {{ bankc | fix4 }}</span>
        </div>
      </div>
      <span class="big_bar username_field">{{ user_id }}</span>
      <span class="big_bar money_bank">{{ currency }} {{ bankc | fix4 }}</span>
      <span class="add-coin" @click="toggleBoxOffice">💌 <span
        class="bubble-x">{{ new_bet_confirmations| notification_code }}</span></span>
      <span class="walletic" @click="toggleWalletX">👛 </span>
      <span v-if="signedinMain" class="singup" @click="sign_in">🔐</span>
      <span v-if="signedinTestNet" class="singup" @click="sign_in">🔐</span>

      <span class="space"></span>
      <span class="right-ex" @click="toggleMusic">{{ music_on ? "🔉" : "🔇" }}</span>
      <span class="right-ex"><nuxt-link to="/">🔙</nuxt-link></span>
    </div>
    <score-card v-show="box_show" @followBet="followBet" @close_x="toggleBoxOffice"/>
    <popupmodal v-if="showModalBetConfirmation"
                @okay_close="after_confirm"
                @cancel_close="showModalBetConfirmation=false">
      <h3 slot="header">🎟下注清單🎟</h3>
      <div slot="body">
        <div v-if="bet_confirmation_bill.rules.length>0">
          <div v-if="bet_confirmation_bill.rules[0]==='simple-a'">
            <table class="table" border="0">
              <tbody>
                <tr>
                  <th>博弈规则:</th>
                  <th>{{ bet_confirmation_bill.rules[0] }}</th>
                </tr>
                <tr>
                  <td>游戏数据源:</td>
                  <td>{{ bet_confirmation_bill.srcid }}</td>
                </tr>
                <tr>
                  <td>开奖期號:</td>
                  <td>{{ bet_confirmation_bill.kjid }}</td>
                </tr>

                <tr>
                  <td>每注價:</td>
                  <td>{{ bet_confirmation_bill.base|fix3 }}</td>
                </tr>
                <tr>
                  <td>x注数:</td>
                  <td>{{ bet_confirmation_bill.bets|fix3 }}</td>

                </tr>
                <tr>
                  <td>x倍数:</td>
                  <td>{{ bet_confirmation_bill.factor|fix3 }}</td>

                </tr>
                <tr class="bottom_lines">
                  <td>总计:</td>
                  <td>{{ bet_confirmation_bill.amount|fix3 }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="bet_confirmation_bill.rules[0].split('-')[0]==='star'">
            <table class="table" border="0">
              <tbody>
                <tr>
                  <td></td>
                  <td></td>
                </tr>
                <tr>
                  <th>博弈规则:</th>
                  <th>{{ bet_confirmation_bill.rules[0] }}</th>
                </tr>
                <tr>
                  <td>游戏数据源:</td>
                  <td>{{ bet_confirmation_bill.srcid }}</td>
                </tr>
                <tr>
                  <td>开奖期號:</td>
                  <td>{{ bet_confirmation_bill.kjid }}</td>
                </tr>
                <tr>
                  <td>每注價:</td>
                  <td>{{ bet_confirmation_bill.base|fix3 }}</td>
                </tr>
                <tr>
                  <td>x注数:</td>
                  <td>{{ bet_confirmation_bill.bets|fix3 }}</td>
                </tr>
                <tr>
                  <td>x倍数:</td>
                  <td>{{ bet_confirmation_bill.factor|fix3 }}</td>
                </tr>
                <tr class="bottom_lines">
                  <td>总计:</td>
                  <td>{{ bet_confirmation_bill.amount|fix3 }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </popupmodal>
  </section>
</template>
<script>
import { mapState } from "vuex"
import { EventBus } from "vue-backgrounds"
import toolUtilSFX from "../../api/mixins/mixin/toolbarSFX"
import animationFloat from "../../api/mixins/mixin/animationFloat"
import ScoreCard from "./ScoreCard"
import Popupmodal from "./popupmodal"

export default {
  name: "Toolbar",
  components: {
    Popupmodal,
    ScoreCard
  },
  mixins: [toolUtilSFX, animationFloat],
  data() {
    return {
      currency: "BTC",
      description: "The next winner is you!",
      display_val: 0.0,
      signedinMain: false,
      signedinTestNet: false,

      box_show: false,
      box_wallet_show: false,
      showModalBetConfirmation: false,

      new_bet_confirmations: 0,
      bet_confirmation_bill: {
        g1: [],
        g2: [],
        g3: [],
        g4: [],
        g5: [],
        kjid: String(this.jk_order_index_number + 1),
        srcid: "",
        timestamp: (new Date()).toISOString(),
        base: 0,
        rules: [],
        bets: 0,
        factor: 0,
        amount: 0,
        testing_mode: false
      }
    }
  },
  computed: {
    ...mapState([
      "user_id",
      "win",
      "lose"
    ]),
    tickets: {
      get() {
        return this.$store.state.kaijiang.tickets
      }
    },
    periodn: {
      get() {
        return parseInt(this.$store.state.kaijiang.kj_period_n)
      }
    },
    status_machine: {
      get() {
        return this.$store.state.kaijiang.status
      }
    },
    bankc: {
      get() {
        return this.$store.state.bank_amount
      },
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      set(newValue) {
      }
    },
    colorp: {
      get() {
        const a = this.$store.state.win && !this.$store.state.lose
        const b = !this.$store.state.win && this.$store.state.lose
        return a || b
      },
      //  setter
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      set(newValue) {
        //        this.$store.state.bank_amount = newValue;
        // const a = this.$store.state.win && !this.$store.state.lose;
        // const b = !this.$store.state.win && this.$store.state.lose;
      }
    }
  },
  mounted() {
    const dat = this
    EventBus.$on("bet_confirm_dialogs", this.before_confirm)
    EventBus.$on("ingamekj", this.getNotification)
    EventBus.$on("bet_confirm", this.getNotification)
    dat.$nextTick(() => {
      dat.getNotification()
    })
  },
  beforeDestroy() {
    this.stopaudio()
    EventBus.$off("bet_confirm_dialogs")
    EventBus.$off("ingamekj")
    EventBus.$off("bet_confirm")
  },
  methods: {
    before_confirm(bet_info) {
      this.bet_confirmation_bill = bet_info
      this.showModalBetConfirmation = true
    },
    after_confirm() {
      this.showModalBetConfirmation = false
      EventBus.$emit("submit_lotto_ticket_exec", this.bet_confirmation_bill)
      this.playNewTicket()
    },
    add_free_coin() {
      this.$store.dispatch("add_coin")
    },
    sign_in() {
      //   this.$store.dispatch ('metamask')
    },
    getNotification() {
      if (this.tickets === undefined) {
        this.new_bet_confirmations = 0
        return
      }
      let h = 0
      const next_ticket_no = this.periodn + 1
      for (let i = 0; i < this.tickets.length; i++) {
        if (parseInt(this.tickets[i].kjid) === next_ticket_no) {
          h++
        }
      }
      console.log("notification # updates", next_ticket_no, " and notification", h)
      this.new_bet_confirmations = h
    },
    home_back() {
    },
    toggleBoxOffice() {
      this.box_show = !this.box_show
    },
    toggleWalletX() {
      this.box_wallet_show = !this.box_wallet_show
    },
    followBet() {
      this.toggleBoxOffice()
    }

  }

  /*
        computed: mapState({
              user_id: (state) => state.user_id,
              user_the_id: 'user_id',
          }), */

  /*  computed: {
              user_id() {
                  return this.$store.state.user_id;
              }
          } */

}
</script>
