<template>
  <div class="SlotMachine">
    <div class="SlotMachine-reels">
      <div class="SlotMachine-shadow"></div>
      <div class="SlotMachine-payline"></div>
      <Reel ref="reel1" :canlock="canlock" @stopped="reelStopped"></Reel>
      <Reel ref="reel2" :canlock="canlock" @stopped="reelStopped"></Reel>
      <Reel ref="reel3" :canlock="canlock" @stopped="reelStopped"></Reel>
    </div>
    <div class="SlotMachine-stats">
      <div class="SlotMachine-coin" @mousedown="insertCoin()"></div>
      <div class="SlotMachine-stat is-credit">
        <div class="SlotMachine-statTitle">Credits</div>
        <div class="SlotMachine-statValue">€ {{ credits.toFixed(2) }}</div>
        <div class="SlotMachine-statSub">spend € {{ spend.toFixed(2) }}</div>
      </div>
      <div class="SlotMachine-stat is-win">
        <div class="SlotMachine-statTitle">Won</div>
        <div class="SlotMachine-statValue">€ {{ win.toFixed(2) }}</div>
      </div>
    </div>
    <div class="SlotMachine-actions">
      <button class="SlotMachine-button is-spin" @mousedown="spin()">Play</button>
      <div :class="{'has-win':win}" class="SlotMachine-button is-win" @mousedown="takeWin()">Take Win
      </div>
    </div>
  </div>
</template>

<script>
import Reel from "@/components/slot333/Reel"
//  import SlotReel from '~/components/slotmachine/reel'
export default {
  name: "SlotMain",
  components: {
    Reel
  },
  data() {
    return {
      spend: 6,
      credits: 6,
      win: 0,
      resultData: false,
      canlock: true,
      waslocked: false,
      audio: {
        win: new Audio("https://freesound.org/data/previews/387/387232_1474204-lq.mp3"),
        insertCoin: new Audio("https://freesound.org/data/previews/276/276091_5123851-lq.mp3"),
        bigwin: new Audio("https://freesound.org/data/previews/270/270319_5123851-lq.mp3")
      }
    }
  },
  computed: {},
  beforeMount() {
  },
  mounted() {
    if (window !== undefined) {
      window.addEventListener("keydown", this.keydown)
    }
  },
  methods: {
    keydown(e) {
      console.log(e.detail)
      const key = {
        one: 49,
        two: 50,
        three: 51,
        space: 32
      }
      if (e.detail === key.one) {
        this.$refs.reel1.lock()
        e.preventDefault()
      } else if (e.detail === key.two) {
        this.$refs.reel2.lock()
        e.preventDefault()
      } else if (e.detail === key.three) {
        this.$refs.reel3.lock()
        e.preventDefault()
      } else if (e.detail === key.space) {
        this.spin()
        e.preventDefault()
      }
    },
    spin() {
      if (this.credits > 0 && !this.resultData) {
        this.resultData = []
        this.credits = this.credits - 0.5
        this.$refs.reel1.run()
        this.$refs.reel2.run()
        this.$refs.reel3.run()
      }
    },
    insertCoin() {
      this.audio.insertCoin.currentTime = 0
      this.audio.insertCoin.play()
      this.credits += 0.5
      this.spend += 0.5
    },
    takeWin() {
      if (this.win > 0) {
        this.credits += this.win
        this.win = 0
      }
    },
    reelStopped(resultData, wasLocked) {
      if (wasLocked) {
        this.waslocked = wasLocked
      }

      this.resultData.push(resultData)
      if (this.resultData.length === 3) {
        this.checkWin(this.resultData)
        if (this.waslocked) {
          this.waslocked = false
          this.canlock = false
        } else {
          this.canlock = true
        }
      }
    },
    checkWin() {
      if (this.resultData.length === 3) { // ;-)
        const v1 = this.resultData[0]
        const v2 = this.resultData[1]
        const v3 = this.resultData[2]
        if (v1.name === v2.name && v2.name === v3.name) {
          if (v1.value >= 10) {
            this.audio.bigwin.play()
          } else {
            this.audio.win.play()
          }
          this.win += v1.value
          this.waslocked = true // prevent lock after an unlocked win
        } else {
          const bar1 = v1.name === "Bar"
          const bar2 = v2.name === "Bar"
          const bar3 = v3.name === "Bar"
          // eslint-disable-next-line no-mixed-operators
          if (bar1 && bar2 || bar1 && bar3 || bar2 && bar3) {
            // this.audio.bigwin.play()
            // this.win += 16
            // this.waslocked = true // prevent lock after an unlocked win
          } else if (bar1 || bar2 || bar3) {
            // this.audio.win.play()
            // this.win += 4
            // this.waslocked = true // prevent lock after an unlocked win
          } else {
            // Lose : (
          }
        }
      }
      this.resultData = false
    }
  }
}
</script>

<style scoped lang="scss">
$tileSize: 90px;

.SlotMachine {
  border-radius: 5px;

  .SlotMachine-reels {
    display: flex;
    position: relative;
  }

  .SlotMachine-shadow {
    border-radius: 4px 4px 0 0;
    pointer-events: none;
    z-index: 99;
    position: absolute;
    width: 100%;
    height: 100%;
    box-shadow: inset 0 25px 30px -5px rgba(0, 0, 0, 0.1),
    inset 0 5px 10px -2px rgba(0, 0, 0, .2),
    inset 0 -25px 30px -5px rgba(0, 0, 0, .1),
    inset 0 -5px 10px -2px rgba(0, 0, 0, .2);
  }

  .SlotMachine-payline {
    position: absolute;
    top: $tileSize * 1 * 1.1666;
    height: 1px;
    width: 100%;
    background: rgba(0, 0, 0, 0.3);
  }

  .SlotMachine-stats {
    display: flex;
    background: #000;
    justify-content: flex-end;
    padding: 10px 0;
  }

  .SlotMachine-coin {
    width: 6px;
    height: 38px;
    background: gray(20);
    border: 3px solid gray(40);
    border-radius: 6px;
    margin: 12px 10px 0 10px;
  }

  .SlotMachine-coin:hover {
    background: gray(140);
  }

  .SlotMachine-stat {
    display: flex;
    flex-direction: column;
    margin-right: 10px;
    flex-grow: 1;
  }

  .SlotMachine-statTitle {
    font-size: 12px;
    color: gray(60);
  }

  .SlotMachine-statValue {
    padding: 5px 10px;
    background: rgba(255, 0, 0, 0.15);
    border-radius: 2px;
    border: 1px solid gray(0);
    font-size: 25px;
    text-align: right;
    color: rgba(255, 0, 0, 0.8);
    text-shadow: 0 1px 5px rgba(255, 0, 0, 0.5);
  }

  .SlotMachine-statSub {
    font-size: 9px;
    color: gray(50);
    text-align: right;
  }

  .SlotMachine-actions {
    padding: 20px 10px;
    display: flex;
    justify-content: flex-end;
    background: gray(20);
    border-radius: 0 0 4px 4px;
  }

  .SlotMachine-button {
    font-size: 17px;
    font-weight: bold;
    padding: 14px 12px;
    margin-left: 20px;
    border-radius: 5px;
    box-shadow: 0 1px 2px 2px gray(0);
  }

  .SlotMachine-button:focus {
    outline: none;
  }

  .SlotMachine-button:active {
    box-shadow: 0 0 2px 1px gray(0);
  }

  .SlotMachine-button.is-spin {
    background: rgba(0, 255, 0, 0.4);
    border: 1px solid rgba(0, 255, 0, 0.4);
  }

  .SlotMachine-button.is-spin:hover {
    background: rgba(0, 255, 0, 0.43);
  }

  .SlotMachine-button.is-spin:active {
    background: rgba(0, 255, 0, 0.46);
  }

  .SlotMachine-button.is-win {
    background: rgba(255, 0, 0, 0.4);
    border: 1px solid rgba(255, 0, 0, 0.5);
  }

  .SlotMachine-button.is-win.has-win {
    background: rgba(255, 0, 0, 0.99);
  }

  .SlotMachine-button.is-win:hover {
    background: rgba(255, 0, 0, 0.65);
  }

  .SlotMachine-button.is-win:active {
    background: rgba(255, 0, 0, 0.7);
  }
}

</style>
