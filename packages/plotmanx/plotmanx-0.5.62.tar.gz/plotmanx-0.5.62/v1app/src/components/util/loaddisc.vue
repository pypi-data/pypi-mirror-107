<template>
  <v-layout v-show="show" padless fluid class="disc-box hazard" color="transparent">
    <v-layout class="topbackground">
    </v-layout>
    <v-layout class="foreground">
      <v-flex v-if="showDisc">
        <v-img>
          <div :class="class_name_pre"></div>
        </v-img>
      </v-flex>
      <v-flex v-show="showLoadingText">
        <h1 class="ytext">
          {{ loadingText }}
        </h1>
      </v-flex>
    </v-layout>
  </v-layout>
</template>
<!--v-show="show"-->
<script>
import { EventBus } from "vue-backgrounds"

export default {
  name: "Loaddisc",
  props: {
    showLoadingText: {
      type: Boolean,
      required: false,
      default: false
    },
    discType: {
      type: String,
      required: false,
      default: "disc"
    },
    show: {
      type: Boolean,
      required: true,
      default: false
    },
    showDisc: {
      type: Boolean,
      required: false,
      default: false
    }
  },
  data: () => ({
    class_name_pre: {
      disc: true,
      record: false,
      black: false,
      bronze: false,
      silver: false,
      gold: false
    },
    loadingText: "",
    preText: ""
  }),
  watch: {
    discType(oldval, nval) {
      this.disc_face(nval)
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.disc_face(this.discType)
    })
    EventBus.$on("loading-message", this._displayMessage)
  },
  beforeDestroy() {
    EventBus.$off("loading-message", this._displayMessage)
  },
  methods: {
    _displayMessage(data) {
      if (this.preText.length > 0) {
        this.loadingText = `${this.preText}${data}`
      } else {
        this.loadingText = data
      }
    },
    onClassOff() {
      this.class_name_pre = {
        disc: true,
        record: false,
        black: false,
        bronze: false,
        silver: false,
        gold: false
      }
    },
    onDiscFace(color) {
      this.onClassOff()
      this.class_name_pre.record = true
      this.class_name_pre[color] = true
    },
    disc_face(nval) {
      if (nval === "black") {
        this.onDiscFace(nval)
      } else if (nval === "bronze") {
        this.onDiscFace(nval)
      } else if (nval === "silver") {
        this.onDiscFace(nval)
      } else if (nval === "gold") {
        this.onDiscFace(nval)
      } else {
        this.onClassOff()
      }
    }
  }
}
</script>

<style lang="scss">
/*https://webgradients.com/*/
$strip_a: #cccccc;
$strip_b: #dbdbdb;
$strip_color: #bc6d0d;
$loading_color: #482b05;
//$loading_banner_height: 15vmin;
$loading_banner_height: 100px;
.disc-box {
  transition-property: opacity;
  transition-duration: .6s;
  transition-timing-function: ease;
  margin: 1em;
  text-align: center;
}

.ytext {
  color: $loading_color;
  font-weight: lighter;
  font-size: 20px;
  font-family: "Roboto-m", -apple-system, Arial, sans-serif;
}

@keyframes animatedBackground {
  from {
    background-position: 0 100%;
  }
  to {
    background-position: 65px 100%;
  }
}

@-webkit-keyframes animatedBackground {
  from {
    background-position: 0 100%;
  }
  to {
    background-position: 65px 100%;
  }
}

@mixin warning_size($hover_color) {
  $strip_a: #cccccc;
  $strip_b: #dbdbdb;
  background-image: repeating-linear-gradient(110deg, $strip_a, $strip_a 30px, $strip_b 30px, $strip_b 60px);
  background-blend-mode: overlay;
  background-color: $hover_color;
  background-repeat: repeat-x;
  animation: animatedBackground 3s linear infinite;
  -webkit-animation: animatedBackground 3s linear infinite;
  background-position: 0 0;
}

.hazard {
  margin: 0;
  height: $loading_banner_height;
  @include warning_size(#d49e3f);
  background-size: 65px $loading_banner_height;
}

.topbackground {
  z-index: 0;
  position: fixed;
  top: 0;

  .content--canvas {
    height: 100px !important;
    overflow: hidden !important;
    width: 100%;

    /*canvas {
      overflow: hidden !important;
      height: 100px !important;
    }*/
  }

}

.foreground {
  z-index: 1;
}

@-webkit-keyframes spin {
  to {
    -webkit-transform: rotate(1turn);
    transform: rotate(1turn);
  }
}

@keyframes spin {
  to {
    -webkit-transform: rotate(1turn);
    transform: rotate(1turn);
  }
}

@mixin square_size($size) {
  width: $size;
  height: $size;
}

@mixin childAnimation($Nth, $time_delay) {
  &:nth-child(#{$Nth}) {
    -webkit-animation-delay: $time_delay;
    animation-delay: $time_delay;
  }
}

@mixin enableHoverPause() {
  &:hover {
    -webkit-animation-play-state: paused;
    animation-play-state: paused;
  }
}

.disc {
  display: inline-block;
  margin: 1em;
  border-radius: 50%;
  -webkit-animation: spin 6s linear infinite;
  animation: spin 6s linear infinite;
  @include square_size(10vmin);

  &.middle {
    @include square_size(30vmin)
  }

  &.large {
    @include square_size(50vmin)
  }

  &.xs {
    @include square_size(80vmin)
  }

  &.enableHover {
    @include enableHoverPause()
  }

  @include childAnimation(1, -1.2s);
  @include childAnimation(2, -2.4s);
  @include childAnimation(3, -3.6s);
  @include childAnimation(4, -4.8s);
  @include childAnimation(5, -6s);

  background-image: radial-gradient(circle, #eee 0, #eee 10%, rgba(17, 17, 17, 0.2) 0, rgba(17, 17, 17, 0.2) 11.5%, rgba(255, 255, 255, 0.25) 0, rgba(255, 255, 255, 0.25) 17%, rgba(17, 17, 17, 0.05) 0, rgba(17, 17, 17, 0.05) 17.5%, rgba(255, 255, 255, 0.25) 0, rgba(255, 255, 255, 0.25) 20%, rgba(17, 17, 17, 0.05) 0, rgba(17, 17, 17, 0.05) 20.5%, rgba(255, 255, 255, 0.25) 0, rgba(255, 255, 255, 0.25) 25%, rgba(17, 17, 17, 0.2) 0, rgba(17, 17, 17, 0.2) 30%, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 69.5%, rgba(17, 17, 17, 0.15) 0, rgba(17, 17, 17, 0.2) 100%), conic-gradient(#ffffff, #f5e1f6, #ffefd1, #fefec5, #c8c8c8, #8a8a8a, #605859, #704864, #3b49ac, #31c8de, #6cd399, #d0d0d0, #fcfcfc, #ffffff, #ffffff, #eafae9, #a3ffef, #98bcea, #9997a4, #868686, #767676, #f0ed5b, #e2a3a7, #d4d4d4, #ffffff, #ffffff);

}

.record {
  &.black {
    background-color: #111;
    background-image: radial-gradient(circle, #eee 0, #eee 1.8%, rgba(17, 17, 17, 0.25) 0, rgba(17, 17, 17, 0.25) 24%, rgba(255, 255, 255, 0) 24%, rgba(255, 255, 255, 0) 100%), conic-gradient(rgba(255, 255, 255, 0.15) 0, rgba(255, 255, 255, 0.15) 5%, rgba(255, 255, 255, 0.25) 8%, rgba(255, 255, 255, 0.25) 18%, rgba(255, 255, 255, 0.05) 24%, rgba(255, 255, 255, 0.05) 32%, rgba(255, 255, 255, 0.1) 34%, rgba(255, 255, 255, 0.1) 42%, rgba(255, 255, 255, 0.05) 46%, rgba(255, 255, 255, 0.05) 56%, rgba(255, 255, 255, 0.15) 64%, rgba(255, 255, 255, 0.15) 69%, rgba(255, 255, 255, 0.05) 72%, rgba(255, 255, 255, 0.05) 81%, rgba(255, 255, 255, 0.1) 84%, rgba(255, 255, 255, 0.1) 86%, rgba(255, 255, 255, 0.05) 90%, rgba(255, 255, 255, 0.05) 95%, rgba(255, 255, 255, 0.15) 98%, rgba(255, 255, 255, 0.15) 100%), radial-gradient(circle, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 29%, rgba(255, 255, 255, 0.05) 0, rgba(255, 255, 255, 0.05) 34.5%, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 35%, rgba(255, 255, 255, 0.05) 0, rgba(255, 255, 255, 0.05) 42%, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 42.5%, rgba(255, 255, 255, 0.05) 0, rgba(255, 255, 255, 0.05) 48%, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 48.25%, rgba(255, 255, 255, 0.05) 0, rgba(255, 255, 255, 0.05) 54.5%, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 55%, rgba(255, 255, 255, 0.05) 0, rgba(255, 255, 255, 0.05) 59%, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 59.5%, rgba(255, 255, 255, 0.05) 0, rgba(255, 255, 255, 0.05) 68%, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 100%);
  }

  &.bronze {
    background-color: #9e501e;
    background-image: radial-gradient(circle, #eee 0, #eee 1.8%, rgba(17, 17, 17, 0.75) 0, rgba(17, 17, 17, 0.75) 24%, rgba(255, 255, 255, 0) 24%, rgba(255, 255, 255, 0) 100%), conic-gradient(rgba(255, 255, 255, 0.45) 0, rgba(255, 255, 255, 0.45) 5%, rgba(255, 255, 255, 0.75) 8%, rgba(255, 255, 255, 0.75) 18%, rgba(255, 255, 255, 0.15) 24%, rgba(255, 255, 255, 0.15) 32%, rgba(255, 255, 255, 0.3) 34%, rgba(255, 255, 255, 0.3) 42%, rgba(255, 255, 255, 0.15) 46%, rgba(255, 255, 255, 0.15) 56%, rgba(255, 255, 255, 0.45) 64%, rgba(255, 255, 255, 0.45) 69%, rgba(255, 255, 255, 0.15) 72%, rgba(255, 255, 255, 0.15) 81%, rgba(255, 255, 255, 0.3) 84%, rgba(255, 255, 255, 0.3) 86%, rgba(255, 255, 255, 0.15) 90%, rgba(255, 255, 255, 0.15) 95%, rgba(255, 255, 255, 0.45) 98%, rgba(255, 255, 255, 0.45) 100%), radial-gradient(circle, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 29%, rgba(255, 255, 255, 0.15) 0, rgba(255, 255, 255, 0.15) 34.5%, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 35%, rgba(255, 255, 255, 0.15) 0, rgba(255, 255, 255, 0.15) 42%, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 42.5%, rgba(255, 255, 255, 0.15) 0, rgba(255, 255, 255, 0.15) 48%, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 48.25%, rgba(255, 255, 255, 0.15) 0, rgba(255, 255, 255, 0.15) 54.5%, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 55%, rgba(255, 255, 255, 0.15) 0, rgba(255, 255, 255, 0.15) 59%, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 59.5%, rgba(255, 255, 255, 0.15) 0, rgba(255, 255, 255, 0.15) 68%, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 100%);
    background-blend-mode: overlay;
  }

  &.silver {
    background-color: #888;
    background-image: radial-gradient(circle, #eee 0, #eee 1.8%, rgba(17, 17, 17, 0.5) 0, rgba(17, 17, 17, 0.5) 24%, rgba(255, 255, 255, 0) 24%, rgba(255, 255, 255, 0) 100%), conic-gradient(rgba(255, 255, 255, 0.3) 0, rgba(255, 255, 255, 0.3) 5%, rgba(255, 255, 255, 0.5) 8%, rgba(255, 255, 255, 0.5) 18%, rgba(255, 255, 255, 0.1) 24%, rgba(255, 255, 255, 0.1) 32%, rgba(255, 255, 255, 0.2) 34%, rgba(255, 255, 255, 0.2) 42%, rgba(255, 255, 255, 0.1) 46%, rgba(255, 255, 255, 0.1) 56%, rgba(255, 255, 255, 0.3) 64%, rgba(255, 255, 255, 0.3) 69%, rgba(255, 255, 255, 0.1) 72%, rgba(255, 255, 255, 0.1) 81%, rgba(255, 255, 255, 0.2) 84%, rgba(255, 255, 255, 0.2) 86%, rgba(255, 255, 255, 0.1) 90%, rgba(255, 255, 255, 0.1) 95%, rgba(255, 255, 255, 0.3) 98%, rgba(255, 255, 255, 0.3) 100%), radial-gradient(circle, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 29%, rgba(255, 255, 255, 0.1) 0, rgba(255, 255, 255, 0.1) 34.5%, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 35%, rgba(255, 255, 255, 0.1) 0, rgba(255, 255, 255, 0.1) 42%, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 42.5%, rgba(255, 255, 255, 0.1) 0, rgba(255, 255, 255, 0.1) 48%, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 48.25%, rgba(255, 255, 255, 0.1) 0, rgba(255, 255, 255, 0.1) 54.5%, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 55%, rgba(255, 255, 255, 0.1) 0, rgba(255, 255, 255, 0.1) 59%, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 59.5%, rgba(255, 255, 255, 0.1) 0, rgba(255, 255, 255, 0.1) 68%, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 100%);
  }

  &.gold {
    background-color: goldenrod;
    background-image: radial-gradient(circle, #eee 0, #eee 1.8%, rgba(17, 17, 17, 0.75) 0, rgba(17, 17, 17, 0.75) 24%, rgba(255, 255, 255, 0) 24%, rgba(255, 255, 255, 0) 100%), conic-gradient(rgba(255, 255, 255, 0.45) 0, rgba(255, 255, 255, 0.45) 5%, rgba(255, 255, 255, 0.75) 8%, rgba(255, 255, 255, 0.75) 18%, rgba(255, 255, 255, 0.15) 24%, rgba(255, 255, 255, 0.15) 32%, rgba(255, 255, 255, 0.3) 34%, rgba(255, 255, 255, 0.3) 42%, rgba(255, 255, 255, 0.15) 46%, rgba(255, 255, 255, 0.15) 56%, rgba(255, 255, 255, 0.45) 64%, rgba(255, 255, 255, 0.45) 69%, rgba(255, 255, 255, 0.15) 72%, rgba(255, 255, 255, 0.15) 81%, rgba(255, 255, 255, 0.3) 84%, rgba(255, 255, 255, 0.3) 86%, rgba(255, 255, 255, 0.15) 90%, rgba(255, 255, 255, 0.15) 95%, rgba(255, 255, 255, 0.45) 98%, rgba(255, 255, 255, 0.45) 100%), radial-gradient(circle, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 29%, rgba(255, 255, 255, 0.15) 0, rgba(255, 255, 255, 0.15) 34.5%, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 35%, rgba(255, 255, 255, 0.15) 0, rgba(255, 255, 255, 0.15) 42%, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 42.5%, rgba(255, 255, 255, 0.15) 0, rgba(255, 255, 255, 0.15) 48%, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 48.25%, rgba(255, 255, 255, 0.15) 0, rgba(255, 255, 255, 0.15) 54.5%, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 55%, rgba(255, 255, 255, 0.15) 0, rgba(255, 255, 255, 0.15) 59%, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 59.5%, rgba(255, 255, 255, 0.15) 0, rgba(255, 255, 255, 0.15) 68%, rgba(255, 255, 255, 0) 0, rgba(255, 255, 255, 0) 100%);
    background-blend-mode: overlay;
  }

}

</style>
