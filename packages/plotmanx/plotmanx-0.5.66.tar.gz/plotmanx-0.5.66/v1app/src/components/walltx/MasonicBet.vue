<template>
  <div class="ugrid clearfix">
    <div class="playfield">

      <div v-if="!_disabled" class="bet-row">
        <div class="invitecodebx half">
          <span class="h2code">Invite Code: <span :class="passed_check_confirmed"> {{ myuplinecode }}</span></span>
        </div>
        <div class="invitecodebx half">
          <input v-model="local_upline_code" :disabled="_disabled" type="text" maxlength="6"/>
        </div>
      </div>

      <div v-if="_disabled" class="bet-row">
        <div class="invitecodebx full">
          <span class="h2code">Invite Code: <span :class="passed_check_confirmed"> {{ myuplinecode }}</span></span>
        </div>
      </div>

      <div class="bet-row">
        <div class="kpocwrpx dark">
          <div :class="{active: level_hazard===btnList.BTN_1}" class="hkyx"
               @click="setBetAmount(btnList.BTN_1)">{{ btnList.BTN_1 }} {{ btnList.UNIT }}
          </div>
          <div :class="{active: level_hazard===btnList.BTN_2}" class="hkyx"
               @click="setBetAmount(btnList.BTN_2)">{{ btnList.BTN_2 }} {{ btnList.UNIT }}
          </div>
          <div :class="{active: level_hazard===btnList.BTN_3}" class="hkyx"
               @click="setBetAmount(btnList.BTN_3)">{{ btnList.BTN_3 }} {{ btnList.UNIT }}
          </div>
          <div :class="{active: level_hazard===btnList.BTN_4}" class="hkyx"
               @click="setBetAmount(btnList.BTN_4)">{{ btnList.BTN_4 }} {{ btnList.UNIT }}
          </div>
          <div :class="{active: level_hazard===btnList.BTN_5}" class="hkyx"
               @click="setBetAmount(btnList.BTN_5)">{{ btnList.BTN_5 }} {{ btnList.UNIT }}
          </div>
        </div>
      </div>

      <div class="content-playfield">
        <div :class="{disabled: cooldown>0 || status_ms !== 4}" class="boxout">
          <span :style="{width: cooldown + '%'}" class="cooldown"></span>
          <button @click="cdown">{{ $t("bnt_bet") }}</button>
        </div>
      </div>
    </div>
    <div class="principle_x">
      <span style="font-size: 5px">{{ $t("bnt_prin") }}:</span>
      <span style="font-size: 9px; color: greenyellow;">{{ principalAmount }}ETH</span>
      <span style="font-size: 5px; color: greenyellow;">{{ wallet_coin }}ETH</span>
    </div>
  </div>
</template>
<script>
import { TimelineLite, Back, Power2, Power1 } from "gsap"
import StringFilter from "../../api/mixins/string_tx"
import ethbasic from "../../api/imple/coreweb3"
import sndbase from "../../api/mixins/capital/audiobase"
import sndmine from "../../api/mixins/capital/cap"

const R_pattern = new RegExp("[`~!@+#$^&*()=|{}':;',\\[\\].<>《》/?~！@#￥……&*（）——|{}【】‘；：”“'。，、？]")
const error_21 = "Non-standard invitation code"

function invalidInviteCode (input) {
  return R_pattern.test(input) || input.length !== 6
}

const ch_list_vals = {
  UNIT: "ETH",
  BTN_1: 1,
  BTN_2: 6,
  BTN_3: 11,
  BTN_4: 15,
  BTN_5: 20
}

export default {
  name: "CxMasonicBet",
  mixins: [sndbase, sndmine, StringFilter, ethbasic],
  data () {
    return {
      local_upline_code: "00FD53",
      input_class: "",
      status_ms: 4,
      bet_amount: 0,
      cooldown: 0,
      passedChecks: false,
      passed_check_confirmed: "failedcheck",
      payout_rate_current: 0,
      level_hazard: 0,
      btnList: ch_list_vals
    }
  },
  computed: {
    _disabled () {
      const result = !this.$store.getters["common/isNewAccount"]
      if (result) {
        // eslint-disable-next-line vue/no-side-effects-in-computed-properties
        this.local_upline_code = ""
      }
      return result
    },
    wallet_coin () {
      return this.$store.getters["wallet/QueryNowBalance"]
    },
    principalAmount () {
      return this.$store.getters["common/principalAmount"]
    },
    change_bet () {
      return this.status_ms !== 4
    },
    myinvitationcode () {
      return this.$store.getters["common/mycode"]
    },
    myuplinecode () {
      return this.$store.getters["common/upline"]
    }
  },
  watch: {
    level_hazard (ol, ne) {
      this.betadjust()
    },
    bet_amount (o, n) {
      this.betadjust()
    },
    local_upline_code (o, n) {
      if (o.length === 6) {
        this.$emit("checkInViteCode", o)
        this.$store.dispatch("common/gen_upline", o)
      } else if (this.$store.getters["common/isNewAccount"]) {
        this.ThisCodeIs(false)
      } else {
        this.ThisCodeIs(true)
      }
    }
  },
  mounted () {
    const timeline = new TimelineLite()
    const that = this
    that.$GSLite = timeline
    const getters = this.$store.getters
    this.$nextTick(() => {
      this.status_ms = 4
      const newacc = getters["common/isNewAccount"]
      if (newacc) {
        this.invite_code = getters["common/upline"]
        this.$emit("checkInViteCode", this.local_upline_code)
      } else {
        this.ThisCodeIs(true)
      }
    })
    /* this.$store.subscribe ((mutations, state) => {
        const { finalpayout } = state.mines.round_game;
        if (finalpayout !== this.payout_rate_current) {
          console.log ("update payout success");
          this.updatePayout (finalpayout, finalpayout > this.payout_rate_current);
        }
      }) */
  },
  methods: {
    setBetAmount (n) {
      const that = this
      if (that.status_ms === 4) {
        that.level_hazard = n
        that.bet_amount = n
      }
    },
    cdown (e) {
      e.preventDefault()
      const that = this
      if (that.cooldown === 0) {
        if (that.bet_amount < 1) {
          that.notificationError("Cannot lower than min")
          that.input_class = "wrong"
          return
        } else {
          that.input_class = ""
        }
        if (!that.passedChecks) {
          that.notificationError(that.$t("n_inv"))
          return
        }
        if (!that._disabled && invalidInviteCode(that.local_upline_code)) {
          that.notificationError(that.$t("n_inv"))
          return
        }
        that.cooldown = 100
        that.$GSLite.to(that, 3, { cooldown: 0 })
        that.status_ms = 1
        that.$GSLite.eventCallback("onComplete", that.cdownComplete)
      }
    },
    cdownComplete () {
      let code = this.local_upline_code
      if (this._disabled) {
        code = this.myuplinecode
      }
      // when all checkers are completed
      this.$emit("invest_submission", {
        amount: parseFloat(this.bet_amount),
        currency: this.coin_symbol,
        invite_code: code,
        time: new Date()
      })
    },
    updatePayout (payrate, up) {
      const that = this; const lite_animation = new TimelineLite()
      // if (that.payout_rate_current < that.payout_rate) {
      lite_animation.to(that, 1.5, { payout_rate_current: payrate })
      if (up) {
        lite_animation.eventCallback("onUpdate", that.sfxPoint)
      }
      // }
    },
    // failed to bet
    // restart to the bet
    setStatusReleased () {
      this.status_ms = 4
      this.input_class = ""
    },
    setStatusConfirmStart () {
      this.notificationSuccess("Game is now Ready!")
      this.status_ms = 2
      this.input_class = "disabled"
    },
    ThisCodeIs (co) {
      this.passedChecks = co
      this.passed_check_confirmed = co ? "passedcheck" : "failedcheck"
    }
  }
}
</script>
<style scoped lang="scss">
  @import "~assets/styles/core/utilities/coloru";
  @import "~assets/styles/core/utilities/fun";
  @import "~assets/styles/core/_bootstrap-variables";
  @import "~assets/styles/core/_animate";

  $colorUpa: #fa9300;
  $colorDowna: #fa6a00;
  $shadowInput: rgba(17, 17, 23, .23);
  $shadowInputFrame: #080808;
  $colorUp: #faee37;
  $colorDown: #c43a02;
  $colorUnderLine: #ffcf22;
  $colorFg: #07cd02;

  .desktop-layout {
    display: -webkit-flex;
    justify-content: center;
    align-items: center;
    align-content: center;
  }

  .principle_x {
    bottom: 10px;
    right: 0px;
    line-height: 20px;
    position: absolute;
    overflow: hidden;
    display: block;
    padding: 5px;
    background-color: $shadowInputFrame;
  }

  .rate_row {
    color: $colorFg;
  }

  .ratex {
    font-family: "Starworld";
  }

  @media(min-width: 510px) {

    .ticker_display {
      font-size: 2em;
      &.count_down_bet {
        font-size: 1.512em;
      }
    }
    .new_balance {
      display: block;
      margin-left: 40px !important;
    }
  }

  @media(max-width: 510px) {
    .ticker_display {
      font-size: 1.1em;
      &.count_down_bet {
        font-size: 0.982em;
      }
    }
  }

  .playfield {
    display: -webkit-flex;
    justify-content: center;
    align-items: center;
    align-content: center;
    flex-flow: column;
  }

  .h2code {
    text-shadow: #1d1d1d -0.7px 1.7px 0.83em;
    color: #2F2F2F;
    font-weight: bold;
    .passedcheck {
      color: $colorUnderLine;
    }
    .failedcheck {
      color: $shadowInputFrame;
    }
  }

  .invitecodebx {
    display: inline-flex;
    font-size: 18px;
    &.half {
      width: 50%;
    }
    &.full {
      width: 100%;
    }

    input[type=number], select[type=number], textarea[type=number] {
      padding-right: 0;
    }

    input {
      background-color: $shadowInput;
      border: 1px solid $shadowInputFrame;
      padding: 0 5px;
      line-height: 46px;
      height: 46px;
      color: #fff;
      font-size: 20px;
      text-align: center;
      width: 100%;
      font-family: "Quicksand", "Source Sans Pro", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      &.wrong {
        border-color: #ff0200 !important;
      }
      box-shadow: 0 0 1em 0.25em rgba(0, 0, 0, .2);
    }
  }

  .btn, button {
    -webkit-appearance: none;
    -moz-appearance: none;
    border: 0;
    -webkit-transition: all .4s ease;
    -moz-transition: all .4s ease;
    -o-transition: all .4s ease;
    transition: all .4s ease;
    display: inline-block;
    cursor: pointer
  }

  .bet-row {
    @include noselect;
    user-select: none;
    border-left: 0;
    border-right: 0;
    flex-shrink: 0;
    padding: 0px;
    height: 70px;
    width: 100%;
    display: flex;
    align-items: center;
    align-content: center;
    color: white;

    .kpocwrpx {
      &.dark {
        background-color: $shadowInput;
      }
      display: flex;
      display: -webkit-flex;
      width: 100%;
      padding: 0 5px;
      .h2 {
        display: block;
        align-items: center;
      }
      .hkyx {
        cursor: pointer;
        font-size: 1.1em;
        line-height: 35px;
        padding-left: 5px;
        padding-right: 5px;
        border-bottom: 1px solid transparent;
        &.active {
          border-color: $colorUnderLine;
        }
      }

    }
  }

  .boxout {
    margin: 20px 0;
    background: linear-gradient(-135deg, $colorUp 0%, $colorDown 100%);
    padding: 2px;
    display: block;
    position: relative;

    .cooldown {
      position: absolute;
      height: 2px;
      background: $colorUp;
      background: linear-gradient(-135deg, $colorUp 0%, $colorDown 100%);
      left: 0;
      bottom: 0;
      z-index: 2;
    }

    button, a {
      text-transform: uppercase;
      width: 100%;
      height: 100%;
      padding: 10px;
      background-color: #080808;
      font-size: 14px;
      font-weight: 700;
      display: flex;
      display: -webkit-flex;
      justify-content: center;
      align-items: center;
      align-content: center;
      transition: all .4s ease;
      text-decoration: none;
      color: $colorUp;
      :hover {
        background-color: transparent;
        color: #000
      }
      .active {
        filter: brightness(0)
      }
      &:before {
        content: "";
        width: 40px;
        height: 40px;
        z-index: 1;
        background: url("~assets/img/appic/ethchw.png") no-repeat 0px 0px;
        background-size: cover;
      }
    }
    .icon {
      margin-right: 10px
    }
    &.disabled, :disabled, .stop {
      background: #1f1b1b;
      button {
        color: $colorDown;
      }
    }
    :hover {
      background-color: transparent;
      color: #000
    }
    &.active {
      //filter: brightness(0)
      background: linear-gradient(-135deg, rgba(159, 158, 160, 0.71) 0%, #212328 100%);
    }
    &.done {
      opacity: .3;
      background: #4ec400
    }
  }

  .balance-wrapper {
    position: relative;
    p {
      font-size: 24px;
      font-weight: 300;
      margin: 0 10px;
      line-height: 20px;

      .symbol-coins {
        color: white;
        &:before {
          width: 1.1em;
          height: 1.1em;
          display: inline-block;
          vertical-align: middle;
          background-size: cover;
          background-image: url("~assets/img/appic/coin_default.png");
          //      background-repeat: no-repeat;
          margin: 0 2px;
          position: relative;
          content: "";
        }
      }
    }

    .new_balance {
      color: $colorUp;
      font-size: 12px;
      line-height: 12px;
      position: absolute;
    }
  }

  .content-playfield {
    margin-top: 20px;
  }

</style>
