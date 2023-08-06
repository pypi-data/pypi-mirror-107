<template>
  <div class="card-container">
    <!--<div class="smallcards">
      <div class="card card-small rotate"></div>
      <div class="card card-small"></div>
    </div>-->
    <div class="mt-1" style="width: 80px; height: 100px; display: inline-block;align-items: center;">
      <varsace name-tag="darksand"/>
    </div>
    <div v-for="(it, i) in list" :key="i" :class="it.class_name">
      <span class="card_rank">{{ it.letter | uppercase }}</span>
    </div>
  </div>
</template>

<script>

export default {
  name: "Cardgen",
  props: {
    code: {
      type: String,
      required: true,
      default: "JQK9"
    },
    right: {
      type: Boolean,
      required: false,
      default: false
    },
    left: {
      type: Boolean,
      required: false,
      default: false
    }
  },
  data() {
    return {
      list: [],
      classes: ["card-hearts", "card-clubs", "card-diams", "card-spades"]
    }
  },
  watch: {
    code(o, n) {
      if (o !== n && n !== "") {
        this.updateCode(n)
      } else if (o !== "" && n === "") {
        this.updateCode(o)
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      if (this.code !== "") {
        this.updateCode(this.code)
        console.log("mounted -- code  ", this.code)
        console.log("mounted -- list  ", this.list)
      }
    })
  },
  destroyed() {
    // console.log("destroy -- code gen")
    // this.updateCode("")
  },
  methods: {
    updateCode(entered_code) {
      const texts = entered_code.split("")
      this.list = _.map(texts, (item) => {
        const r = _.random(0, 3)
        const cardface = [
          "card",
          this.classes[_.floor(r)],
          this.right ? "card-small--right" : "",
          this.left ? "card-small--left" : ""
        ]
        return {
          letter: item,
          class_name: cardface.join(" ")
        }
      })
    }
  }
}
</script>

<style lang="scss">

// @import url(https://fonts.googleapis.com/css?family=Open+Sans);

/*colors*/

$greenBackground: #d7926c;
$table: $greenBackground;
$grey: #434A54;
$red: #FC6E51;
$purple: #967ADC;
$yellow: #ffee6c;
$pink: #EC87C0;

a:active {
  /*remove all the Dotted Link Borders*/
  outline: none;
}

/*
 Spade : \2660
heart: \2665
diamond: \2666
club: \2663
 */

.poker_card_container_basic {
  overflow: hidden;
  position: relative;
  align-items: center;
}

@media(max-width: 599px) {
  .card-container {
    height: 100px;
    padding-top: 8px;
  }
}

@media(min-width: 600px) {
  .card-container {
    min-height: 200px;
    padding: 86px;
  }
}

/*

$breakpointlistpokercard: (
  r1: (510px, 86px),
  r2: (414px, 86px),
  r3: (411px, 86px),
  r4: (375px, 86px),
  r5: (360px, 86px),
  r6: (320px, 86px),
) !default;

@each $bp in $breakpointlistpokercard {
  $width-device: nth($bp, 1);
  $padding: nth($bp, 2);
  @media(max-width: $width-device) {
    .card-container {
    }
  }
}
*/

.card-container {
  @extend .poker_card_container_basic;
  color: #333;
  background-color: $greenBackground;
  font-size: 0.226em;
  padding-left: 10px;
  /*card module*/
  .smallcards {
    top: 13px;
    left: 310px;
    position: relative;
    z-index: 3;
  }

  .card {
    font-family: 'varsace-b', 'versace', 'Prida', sans-serif;
    position: relative;
    z-index: 2;

    display: table;
    float: left;

    width: 58px;
    height: 81px;
    margin: 0 5px 0 1px;

    border-radius: .8em;
    background-color: #fff;
    box-shadow: 3px 4px 0 rgba(0, 0, 0, 0.2);

    .card_rank {
      position: relative;
      font-size: 9em;
      font-weight: bold;
      line-height: 1em;
      display: table-cell;
      text-align: center;
      vertical-align: middle;
    }

    .card_rank:before {
      width: 100%;
      height: 1em;
      display: block;
      text-align: center;
    }

    &.card-spades {
      .card_rank:before {
        /*spade*/
        content: "🍀";
      }
    }

    &.card-diams {
      color: $red;

      .card_rank:before {
        /*spade*/
        content: "🌸";
      }
    }

    &.card-hearts {
      color: $yellow;

      text-shadow: 0 0 6px rgb(0 0 0);
      .card_rank:before {
        /*spade*/
        content: "🎩";
      }
    }

    &.card-clubs {
      .card_rank:before {
        /*spade*/
        content: "🌹";
      }
    }

    &.card-small--left,
    &.card-small--right {
      font-size: 0.5em;
      height: 41px;

      position: absolute;
      top: 190px;
      width: 28px;
    }

    &.card-small--left {
      left: 186px;
    }

    &.card-small--right {
      left: 222px;
    }

    &.card-small {
      background-color: #8cf523;
      box-shadow: none;
      height: 35px;
      left: 36px;
      top: 9px;
      position: absolute;
      width: 25px;
      z-index: 1;

      &:before,
      &:after {
        background-color: #fc6e51;
        border: 3px solid #fff;
        border-radius: 50%;
        content: "";
        height: 15px;
        width: 15px;
        position: absolute;
        z-index: 1;
      }

      &:before {
        left: 35px;
        top: -4px;
      }

      &:after {
        left: 34px;
        top: 6px;
        z-index: 2;
        background-color: $purple;
      }

      &.rotate {
        box-shadow: 3px 4px 0 rgba(0, 0, 0, 0.2);
        left: 21px;
        top: 10px;
        z-index: 2;
        -ms-transform: rotate(-29deg); /* IE 9 */
        -webkit-transform: rotate(-29deg); /* Chrome, Safari, Opera */
        transform: rotate(-29deg);

        &:before {
          background-color: #ffce54;
          left: 42px;
          top: 35px;
          transform: rotate(0deg);
        }

        &:after {
          background-color: #ec87c0;
          left: 37px;
          top: 43px;
          transform: rotate(0deg);
          z-index: 2;
        }
      }
    }
  }

}

</style>
