<template>
  <div class="wgrid clearfix">
    <div class="row rate_row">
      <div class="col col-2-of-4">RATE X</div>
      <div class="col col-2-of-4 ratex">{{ payout_rate_current|fix3 }}</div>
    </div>
    <div class="long-bet betting">
      <div class="desktop-layout">
        <div class="chesticon"></div>
        <div class="balance-wrapper">
          <p class="balance"><span class="text-nowrap"><span class="symbol symbol-coins">{{
              coin_symbol|coinName
            }}</span></span>
          </p>
          <p class="new_balance">{{ wallet_coin }}</p>
        </div>
        <input :class="input_class" v-model="bet_amount" :disabled="change_bet" type="number"
               name="amount"
               placeholder="Minimum bet is 10"
               autocomplete="off"/>
      </div>
    </div>
    <div class="playfield">
      <div class="bet-row">
        <div class="bombs">
          <div :class="{active: level_hazard===1}" class="bomb" @click="switchLevel(1)">1</div>
          <div :class="{active: level_hazard===3}" class="bomb" @click="switchLevel(3)">3</div>
          <div :class="{active: level_hazard===5}" class="bomb" @click="switchLevel(5)">5</div>
          <div :class="{active: level_hazard===24}" class="bomb" @click="switchLevel(24)">24</div>
        </div>
        <div :class="{disabled: cooldown>0 || status_ms !== 4}" class="boxout">
          <span :style="{width: cooldown + '%'}" class="cooldown"></span>
          <button @click="cdown">play</button>
        </div>
      </div>
      <div class="content-playfield">
        <slot name="content-play">
          default game play
        </slot>
      </div>
    </div>
  </div>
</template>

<script>
import { TimelineLite, Back, Power2, Power1 } from "gsap"

//import sndbase from "../../plugins/mixins/minesweep/audiobase"
//import sndmine from "../../plugins/mixins/minesweep/miniGameMines"
/*
    declare_const : {
        BET_AWAITING : 1,
        GAME_IN_PLAY : 2,
        GAME_OPENED_BET : 4,
    }

    */

export default {
  name: "FieldBet",
  components: {},
  mixins: [sndbase, sndmine, string_tx],
  data() {
    return {
      input_class: "",
      status_ms: 4,
      autoplays: 1,
      bet_amount: 0,
      wallet_coin: 0,
      coin_symbol: "---",
      cooldown: 0,
      payout_rate_current: 0,
      level_hazard: 0
    }
  },
  computed: {
    bankRolls: {
      get() {
        return this.$store.getters["mines/MinePots"]
      }
    },
    payout_rate: {
      get() {
        return this.$store.getters["mines/Payout"]
      }
    },
    change_bet() {
      return this.status_ms !== 4
    }
  },
  watch: {
    level_hazard(ol, ne) {
      this.betadjust()
    },
    bet_amount(o, n) {
      this.betadjust()
    }
  },
  mounted() {
    const timeline = new TimelineLite()
    const that = this
    that.$GSLite = timeline
    const getters = that.$store.getters
    that.$nextTick(() => {
      console.log(getters)
      that.coin_symbol = getters["mines/QueryFirstWalletSymbolMineGame"]
      that.wallet_coin = getters["mines/QueryFirstWalletCoinAmountMine"]
      that.status_ms = 4
      that.$store.subscribe((mutations, state) => {
        const { finalpayout } = state.mines.round_game
        if (finalpayout !== that.payout_rate_current) {
          console.log("update payout success")
          that.updatePayout(finalpayout, finalpayout > that.payout_rate_current)
        }
      })
    })
  },
  methods: {
    switchLevel(n) {
      const that = this
      if (that.status_ms === 4) {
        that.level_hazard = n
      }
    },
    cdown() {
      const that = this
      if (that.cooldown === 0) {
        that.cooldown = 100
        that.$GSLite.to(that, 3, { cooldown: 0 })
        // console.log ("cdown works");

        if (this.status_ms === 2) {
          // alert, success, error, warning, info
          that.notificationError("Game is now in play")
          // console.log ("status_ms block");
          return
        }

        if (that.bet_amount < 10) {
          that.notificationError("Invalid bet amount")
          // console.log ("amount block");
          that.input_class = "wrong"
          return
        } else {
          that.input_class = ""
        }

        if (that.autoplays < 1) {
          that.notificationError("Autoplay invalid")
          // console.log ("autoplay block");
          return
        }

        if (that.level_hazard <= 0) {
          that.notificationError("Monster amount invalid")
          return
        }

        if (that.coin_symbol === "---") {
          that.notificationError("Coin name is invalid")
          return
        }
        that.status_ms = 1
        that.$GSLite.eventCallback("onComplete", that.cdownComplete)
      }
    },
    cdownComplete() {
      // when all checkers are completed
      this.$emit("now_play", {
        plays: this.autoplays,
        amount: parseFloat(this.bet_amount),
        currency: this.coin_symbol,
        level: this.level_hazard,
        time: new Date()
      })
    },
    updatePayout(payrate, up) {
      const that = this
      const lite_animation = new TimelineLite()
      // console.log ("update payout");
      // if (that.payout_rate_current < that.payout_rate) {
      lite_animation.to(that, 1.5, { payout_rate_current: payrate })
      if (up) {
        lite_animation.eventCallback("onUpdate", that.sfxPoint)
      }
      // }
    },
    // failed to bet
    // restart to the bet
    setStatusReleased() {
      this.status_ms = 4
      this.input_class = ""
    },
    setStatusConfirmStart() {
      this.notificationSuccess("Game is now Ready!")
      this.status_ms = 2
      this.input_class = "disabled"
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

$colorUp: #84c5fa;
$colorDown: #327cfa;
$colorFg: #a3ebf8;

.desktop-layout {
  display: -webkit-flex;
  justify-content: center;
  align-items: center;
  align-content: center;
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

.long-bet {

  input {
    width: 70px;
    margin: 0 20px;
  }

  .chesticon {
    width: 64px;
    height: 64px;
    background-image: url("~assets/img/whitechest.png");
    background-size: cover;
    position: relative;
    display: flex;
    /* .gradientcolor {
       background: linear-gradient(-135deg, $colorUp 0%, $colorDown 100%);
       mix-blend-mode: multiply;
       display: block;
       position: absolute;
       width: 128px;
       height: 64px;

     }
     img {
       width: 64px;
       height: 64px;
       position: absolute;
       margin: 0px;
       padding: 0px;
     }*/
  }

}

input[type=number], select[type=number], textarea[type=number] {
  padding-right: 0;
}

input {
  background-color: rgba(17, 17, 23, .23);
  border: 1px solid #080808;
  padding: 0 10px;
  line-height: 46px;
  height: 46px;
  color: #fff;

  &.wrong {
    border-color: #ff0200 !important;
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
  background-color: #080808;
  border: 1px solid #151515;
  border-left: 0;
  border-right: 0;
  flex-shrink: 0;
  width: 400px;
  min-width: 100%;
  height: 70px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  align-content: center;
  color: white;

  .bombs {
    display: flex;
    display: -webkit-flex;
    justify-content: center;
    align-items: center;
    align-content: center;
    margin: 0 20px;

    .bomb {
      height: 70px;
      line-height: 70px;
      cursor: pointer;
      font-size: 16px;
      display: block;
      padding: 0 0 0 45px;
      margin-left: 0px;
      background: url("~assets/img/kraken_alive.png") no-repeat 0 30px;
      background-position: 13px 50%;
      background-size: 25px 25px;
      border-bottom: 1px solid transparent;

      &.active {
        border-color: $colorDown;
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
      //        filter: brightness(0)
      background: linear-gradient(-135deg, rgba(159, 158, 160, 0.71) 0%, #212328 100%);
    }

    &.done {
      opacity: .3;
      background: #4ec400
    }
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
        background-image: url("~assets/img/coin_default.png");
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
