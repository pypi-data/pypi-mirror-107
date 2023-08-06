<template>
  <section class="toolbar container-fluid">
    <div class="flex-row">
      <div class="small_bar">
        <div class="small_box">
          <span class="username_f">{{ user_id }}</span>
          <span class="moneybank_f">{{ currency }} {{ bankc | fix4 }}</span>
        </div>
      </div>
      <span class="big_bar username_field">{{ user_id }}</span>
      <span class="big_bar money_bank">{{ currency }} {{ bankc | fix4 }}</span>
      <span class="add-coin" @click="add_free_coin">💌</span>
      <span v-if="signedinMain" class="singup" @click="sign_in">🔐</span>
      <span v-if="signedinTestNet" class="singup" @click="sign_in">🔐</span>
      <!--
                        <div class="color_label">
                            <input type="checkbox" name="slider" class="slider-checkbox" id="sliderSwitch">
                            <label class="slider-label" for="sliderSwitch">
                                <span class="slider-inner"></span>
                                <span class="slider-circle"></span>
                            </label>
                        </div>
            -->
      <span class="space"></span>
      <span class="right-ex" @click="toggleMusic">{{ music_on?"🔉":"🔇" }}</span>
      <span class="right-ex"><nuxt-link to="/">🔙</nuxt-link></span>
    </div>
  </section>
</template>

<style lang="scss" scoped>
    $tron: #0DFF92;
    .flex-row {
        display: flex;
        flex-direction: row;
    }

    .small_bar {
        display: inline-block;
        padding-left: 11px;
    }

    .small_box {
        display: flex;
        flex-direction: column;
        font-size: .1em;
        color: $tron;
        width: auto;
        .username_f {
            order: 1;
            flex: 1;
            display: block;
        }
        .moneybank_f {
            order: 2;
            flex: 1;
            display: block;
        }

    }

    @media(min-width: 510px) {
        .small_box {
            display: none;
        }
    }

    .toolbar {
        box-shadow: 0px 2px 4px -1px rgba(0, 0, 0, 0.2), 0px 4px 5px 0px rgba(0, 0, 0, 0.14), 0px 1px 10px 0px rgba(0, 0, 0, 0.12);
        position: fixed;
        width: 100%;
        background-color: rgba(42, 34, 10, 0.67);
        z-index: 100;
    }

    .username_field {
        display: inline-block;
        padding-left: 10px;
        padding-right: 10px;
        font-size: 1.2em;
        font-family: "Impact",serif;
        vertical-align: bottom;
        color: #0DFF92;
    }

    .money_bank {
        display: inline-block;
        padding-left: 10px;
        padding-right: 10px;
        font-size: large;
        background-color: #6f5505;
        color: #eec509;
    }

    @media(max-width: 510px) {
        .big_bar {
            display: none;
        }
        .small_bar {
            flex: 4;
        }
    }

    .add-coin {
        cursor: pointer;
        display: inline;
        padding-left: 3px;
        padding-right: 3px;
        flex: 1;
        text-align: center;
        text-decoration: none;
        font-size: large;
        background-color: #b4a329;
    }

    .right-ex {
        text-align: center;
        cursor: pointer;
        display: inline;
        padding-left: 5px;
        padding-right: 5px;
        text-decoration: none;
        font-size: large;
        color: #f1df37;
        background-color: #b4a329;
        flex: 1;
    }

    .space {
        flex: 5;
    }

    @media(min-width: 510px) {
        .space {
            flex: 10;
        }
    }

    .singup {
        cursor: pointer;
        display: inline-block;
        padding-left: 10px;
        padding-right: 10px;
        text-decoration: none;
        font-size: large;
        color: #f18453;
        background-color: #b47a38;
    }

</style>
<script>
import { mapState } from "vuex"

export default {
  name: "Toolbar",
  data () {
    return {
      currency: "BTC",
      description: "The next winner is you!",
      display_val: 0.0,
      signedinMain: false,
      signedinTestNet: false,
      loop: {
        main: new Audio("/media/monster_strike_main.mp3"),
        sp1: new Audio("/media/monster_strike_main.mp3"),
        sp3: new Audio("/media/monster_strike_main.mp3"),
        spafter: new Audio("/media/monster_strike_main.mp3"),
        spaftq: new Audio("/media/monster_strike_main.mp3")
      },
      music_clip_pos: 0,
      music_on: false,
      current_music: null
    }
  },

  computed: {
    ...mapState([
      "user_id",
      "win",
      "lose"
    ]),
    status_machine: {
      get () {
        return this.$store.state.kaijiang.status
      }
    },
    cprofit: {
      get () {
        return this.$store.state.cprofit
      },
      set (newValue) {
      }
    },
    bankc: {
      get () {
        return this.$store.state.bank_amount
      },
      set (newValue) {
      }
    },
    colorp: {
      get () {
        const a = this.$store.state.win && !this.$store.state.lose
        const b = !this.$store.state.win && this.$store.state.lose
        return a || b
      },
      //  setter
      set (newValue) {
        //        this.$store.state.bank_amount = newValue;
        // const a = this.$store.state.win && !this.$store.state.lose;
        // const b = !this.$store.state.win && this.$store.state.lose;
      }
    }
  },
  watch: {
    cprofit (val) {
      const a = this.bankc - val; const b = this.bankc; const dat = this
      // dat.$store.commit('update_bank_amount', b);
      // if (b < 0) return;
      /*   setTimeout(() => {
                       dat.animateValue(a, b, 1000,
                           (s) => {
                               dat.display_val = s;
                           }, () => {
                           });
                   }, 1000); */
    }
  },
  mounted () {
    const dat = this
    dat.$nextTick(() => {
      /* var web3object = this.$store.state.web3;
                 var k = web3object.isInjected && web3object.networkId === "main";
                 if (k) {
                     dat.signedinMain = true;
                     dat.signedinTestNet = false;
                 } else {
                     dat.signedinMain = false;
                     dat.signedinTestNet = true;
                 } */
    })
  },
  beforeDestroy () {
    this.stopaudio()
  },
  methods: {
    add_free_coin () {
      this.$store.dispatch("add_coin")
    },
    sign_in () {
      //   this.$store.dispatch ('metamask')
    },
    home_back () {

    },
    toggleMusic () {
      if (!this.music_on) {
        this.playMusic()
      } else {
        this.stopaudio()
      }
    },
    playMusic () {
      const index = this.nextLoop()
      this.getLoop()[index].play()
      this.music_on = true
      this.current_music = this.getLoop()[index]
    },
    stopaudio () {
      if (this.current_music instanceof Audio) {
        this.current_music.pause()
        this.current_music.currentTime = 0
        this.music_on = false
      }
    },
    nextLoop () {
      this.music_clip_pos++
      return this.music_clip_pos % this.getLoop().length
    },
    getLoop () {
      if (this.status_machine === 1 || this.status_machine === 0) {
        return [this.loop.main, this.loop.sp1, this.loop.sp3]
      } else {
        return [this.loop.spafter, this.loop.spaftq]
      }
    },
    animateValue (oldVal, newValue, duration, funcUpdate, funcDone) {
      let currentVal = oldVal
      const diff = newValue - oldVal
      const range = diff / 0.0001
      const minTime = 50
      const stepTime = Math.max(Math.abs(Math.floor(duration / range)), minTime)
      // console.log("stepTime:,", stepTime);
      const startTime = new Date().getTime()
      const endTime = startTime + duration

      let timer = 0

      function run () {
        const now = new Date().getTime()
        const remaining = Math.max((endTime - now) / duration, 0)
        const value = newValue - (remaining * diff)
        // console.log("u:,", remaining, value);
        currentVal = value
        funcUpdate(currentVal)
        if (value === newValue) {
          clearInterval(timer)
          if (funcDone !== undefined) { funcDone() }
        }
      }

      clearInterval(timer)
      timer = setInterval(run, stepTime)
      run()
    }

  }

}
</script>
