<template>
  <div class="roulette">
    <div id="rulx-scroll-box-wrapper">
      <div id="scroll" :style="styleObject.scroller" class="roulette-scroll">
        <div v-for="k in repeat_full" :key="k" class="r-reel-row">
          <div v-for="v in roulette_max_num" :key="v" class="r-box">{{ v }}</div>
        </div>
      </div>
      <div class="roulette-indicator"></div>
      <!--   <div :v-if="debug_ds" class="roulette-debugv">{{ rx_x }}, {{ out_display }}, {{ target_n }}</div>
     -->
    </div>
  </div>
</template>
<script>
import colorx from "@/api/mixins/mixin/colorx"
import { TweenMax, Power4, Power2 } from "gsap"
import { EventBus } from "vue-backgrounds"

export default {
  name: "Reellet",
  mixins: [colorx],
  props: {
    box_w: {
      type: Number,
      required: false,
      default: 50
    },
    roulette_max_num: {
      type: Number,
      required: false,
      default: 37
    },
    debug_ds: {
      type: Boolean,
      required: false,
      default: false
    }
  },
  data() {
    return {
      repeat_full: 10,
      item_full: 0,
      items: [],
      rolling: false,
      ready_roll_again: true,
      out_display: 0,
      rx_x: 0,
      run_tl: 0,
      target_n: 0,
      styleObject: {
        scroller: {},
        timerDiv: {},
        buttonStatus: "active"
      },
      audio: {
        chip: new Audio("https://freesound.org/data/previews/440/440619_9054991-lq.mp3")
      }
    }
  },
  mounted() {
    const box_w = this.box_w
    const num = this.roulette_max_num
    const repeat = this.repeat_full
    this.$nextTick(() => {
      // const w = document.getElementById("rulx-scroll-box-wrapper").clientWidth
      // const box_w = document.getElementsByClassName("r-box").clientWidth
      // margin-left: calc(250px - 25px - (1450px * 1) - (50px * 0));
      const item_full = num * box_w
      // const init_position_c = w - box_w / 2 - box_w - item_full * repeat / 2
      const init_position = -item_full * 2
      this.item_full = item_full
      TweenMax.set(".roulette-scroll", {
        width: `${item_full * repeat}px`,
        "margin-left": `${init_position}px`
      })
      TweenMax.set(".r-reel-row", {
        width: `${item_full}px`
      })
      EventBus.$on("reel_roll_state_check", this.roll_start)
      EventBus.$on("reel_roll_callback_result", this.roll_stop)
      const { play } = this.$store.getters["roulette/yf_flags"]
      if (play) {
        this.roll_start()
      }
    })
  },
  beforeDestroy() {
    EventBus.$off("reel_roll_state_check", this.roll_start)
    EventBus.$off("reel_roll_callback_result", this.roll_stop)
    this.rolling = false
    this.ready_roll_again = true
  },
  methods: {
    getStateRolling() {
      return {
        rolling: this.rolling,
        roll_again: this.ready_roll_again
      }
    },
    roll_start() {
      if (this.rolling) {
        return
      }
      if (!this.ready_roll_again) {
        return
      }
      this.rolling = true
      this.ready_roll_again = false
      this.run_tl = this.getEngine().to(".roulette-scroll", 2.8, {
        "margin-left": `+=${this.item_full}`,
        modifiers: {
          "margin-left": this.displacement()
        },
        ease: "none",
        onUpdate: this.displaceUpdate,
        repeat: -1
      })
      this.$emit("reel_roll_state_rolling")
    },
    roll_stop(N) {
      if (!this.rolling) {
        return
      }
      const offset_target_n = 3
      const boxWidth = this.box_w
      this.ready_roll_again = false
      this.rolling = false
      this.run_tl.pause()
      let rx = 0
      let v = 0
      this.target_n = N
      let rollatpos = this.rx_x
      let dx_roll = 0
      while (rollatpos < 0) {
        rollatpos += this.item_full
      }
      while (rx < rollatpos) {
        rx = -boxWidth * (N - offset_target_n) + this.item_full * v
        v++
      }
      dx_roll = rx - this.rx_x
      this.run_tl = this.getEngine().to(".roulette-scroll", 10, {
        "margin-left": `${this.rx_x + dx_roll}px`,
        modifiers: {
          "margin-left": this.displacement()
        },
        ease: Power4.easeOut,
        onUpdate: this.displaceUpdate,
        repeat: 0
      }).call(() => {
        this.ready_roll_again = true
        // this.audio.clip.play()
        this.$emit("reel_roll_complete")
      })
    },
    stop_debug() {
      const ek = Math.floor(Math.random() * 36) + 1
      console.log(ek)
      this.roll_stop(ek)
    },
    stop_fixed() {
      if (!this.rolling) {
        return
      } else {
        this.rolling = false
      }
      // const repeats = Math.floor(this.run_tl.totalTime() / this.run_tl.duration())
      // console.log(this.run_tl.totalTime())
      this.run_tl.pause()
      this.run_tl = this.getEngine().to(".roulette-scroll", 5, {
        "margin-left": `${this.rx_x + 1000}px`,
        modifiers: {
          "margin-left": this.displacement()
        },
        ease: Power2.easeOut,
        onUpdate: this.displaceUpdate,
        repeat: 0
      })
    },
    displacement() {
      return this.GSAP().utils.unitize((x) => {
        if (x > -this.item_full) {
          return parseFloat(x) - this.item_full * (this.repeat_full - 3)
        } else {
          return parseFloat(x) % (this.item_full * this.repeat_full)
        }
      })
    },
    displaceUpdate() {
      this.rx_x = this.GSAP().getProperty(".roulette-scroll", "margin-left")
      this.out_display = Math.abs(this.rx_x % this.item_full) / 50 + 1
    },
    getEngine() {
      return this.$gsapTimeLine({
        defaults: {
          duration: 0.8,
          ease: Power4.easeInOut
        }
      })
    }
  }
}
</script>
<style lang="scss">
$width_total: 1450px;
$green_background: rgba(0, 91, 0, 0.75);
$green_background_shadow: rgb(0, 62, 0);

.roulette {
  width: 100%;
  margin-top: 25px;
  height: 100px;
  margin-left: 0;
  margin-right: 0;
  overflow: hidden;
  position: relative;

  .roulette-debugv {
    position: absolute;
    z-index: 2;
    background-color: whitesmoke;
    right: 5px;
    font-size: x-small;
    line-height: inherit;
  }

  .roulette-indicator {
    position: absolute;
    left: 125px;
    margin: 0;
    width: 1px;
    height: 50px;
    background-color: #fff;
    z-index: 1;
  }

  /*
    background-image: radial-gradient($green_background, black 120%);

    &::after {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100%;
      background: repeating-linear-gradient(
              0deg,
              rgba(black, 0.15),
              rgba(black, 0.15) 1px,
              transparent 1px,
              transparent 2px
      );
      pointer-events: none;
    }*/

  .roulette-scroll {
    position: absolute;
    height: 50px;
    margin-top: 0;
    overflow: hidden;

    .r-reel-row {
      height: 50px;
      background: #f8d41c;
      float: left;

      .r-box {
        width: 50px;
        height: 50px;
        line-height: 50px;
        text-align: center;
        color: #fff;
        float: left;
        font-weight: 700;
        font-family: Montserrat, "Open Sans", Helvetica, Arial, sans-serif;

        &:nth-child(1) {
          background: green !important;
        }

        &:nth-child(odd) {
          background: #313131;
        }

        &:nth-child(even) {
          background: red;
        }
      }
    }

  }

}

</style>
