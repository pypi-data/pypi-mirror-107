<template>
  <div :class="{'is-locked':locked}" class="Reel" @mousedown="lock()">
    <div class="Reel-inner">
      <img :src="reelTileData[tile1Index].image" class="Reel-image"/>
      <img :src="reelTileData[tile2Index].image" class="Reel-image"/>
      <img :src="reelTileData[tile3Index].image" class="Reel-image"/>
      <img :src="reelTileData[tile4Index].image" class="Reel-image"/>
      <img :src="reelTileData[tile5Index].image" class="Reel-image"/>
    </div>
  </div>
</template>

<script>
export default {
  name: "Reel",
  props: {
    value: {
      type: Number,
      required: true,
      default: 1
    },
    right: {
      type: Boolean,
      required: false,
      default: false
    },
    canlock: {
      type: Boolean,
      required: false,
      default: false
    }
  },
  data() {
    return {
      momentum: null,
      audio: {
        spin: new Audio("https://freesound.org/data/previews/120/120373_824230-lq.mp3"),
        spinEnd: new Audio("https://freesound.org/data/previews/145/145441_2615119-lq.mp3"),
        lock: new Audio("https://freesound.org/data/previews/56/56246_91374-lq.mp3")
      },
      reelTileCount: 15,
      reelTileData: null,
      reelSourceData: [
        {
          name: "Lemon",
          value: 2,
          image: "https://cdn4.iconfinder.com/data/icons/slot-machines/512/Lemon-512.png"
        },
        {
          name: "Melon",
          value: 4,
          image: "https://cdn4.iconfinder.com/data/icons/slot-machines/512/Watermelon-512.png"
        },
        {
          name: "Grapes",
          value: 10,
          image: "https://cdn4.iconfinder.com/data/icons/slot-machines/512/Grapes-512.png"
        },
        {
          name: "Cherry",
          value: 16,
          image: "https://cdn4.iconfinder.com/data/icons/slot-machines/512/Cherry-512.png"
        },
        {
          name: "Bar",
          value: 32,
          image: "https://cdn4.iconfinder.com/data/icons/casino-games/512/bar-512.png"
        }
      ],
      reelIndex: 2,
      tile1Index: 0,
      tile2Index: 1,
      tile3Index: 2,
      tile4Index: 3,
      tile5Index: 4,
      locked: false
    }
  },
  computed: {},
  beforeMount() {
    // Build up the reelTileData array with random tiles
    const frs = []
    const count = this.reelTileCount
    this.audio.spin.volume = 0.3
    this.audio.spinEnd.volume = 0.8
    this.audio.lock.volume = 0.2
    this.audio.spin.currentTime = 0.3
    // Method 1, random until count is reached
    // while (count > 0) {
    //   const fruitIndex = Math.floor(Math.random() * this.reelSourceData.length)
    //   const fruitObject = this.reelSourceData[fruitIndex]
    //   frs.push(fruitObject)
    //   count--
    // }

    // Method 2, sort on value, use index to determine entry count, shuffle
    const reelSourceData = this.reelSourceData.slice(0)
    reelSourceData.sort((a, b) => b.value - a.value)
    reelSourceData.forEach((sd, i) => {
      let times = i + 1 + i // 0+1+0=1, 3+2+3=8
      while (times > 0) {
        frs.push(sd)
        times--
      }
    })

    function shuffle(array) {
      let currentIndex = array.length
      let temporaryValue
      let randomIndex

      // While there remain elements to shuffle...
      while (currentIndex !== 0) {
        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex)
        currentIndex -= 1

        // And swap it with the current element.
        temporaryValue = array[currentIndex]
        array[currentIndex] = array[randomIndex]
        array[randomIndex] = temporaryValue
      }

      return array
    }

    this.reelTileData = shuffle(frs)
  },
  mounted() {
    this.$el.addEventListener("transitionend", this.animateEnd)
  },
  methods: {
    run() {
      console.log("run")
      if (!this.locked) {
        const min = 8
        const max = 28
        this.momentum = Math.floor(Math.random() * (max - min + 1) + min)
        this.audio.spin.play()
        this.animate()
      } else {
        this.locked = false
        this.$emit("stopped", this.reelTileData[this.reelIndex], true)
      }
    },
    animate() {
      this.$el.classList.add("move")
    },
    animateEnd() {
      this.$el.classList.remove("move")
      this.reIndex()
      this.momentum = this.momentum - 1
      if (this.momentum > 0) {
        setTimeout(this.animate, 10)
      } else {
        this.$emit("stopped", this.reelTileData[this.reelIndex])
        this.audio.spinEnd.play()
        this.audio.spin.pause()
        this.audio.spin.currentTime = 0.3
      }
    },
    reIndex() {
      const end = this.reelTileData.length - 1 // this.reelTileCount - 1
      const index = this.reelIndex === 0 ? end : this.reelIndex - 1
      // const index = this.index === end ? 0 : this.index + 1
      this.reelIndex = index
      this.tile1Index = index === 1 ? end : index === 0 ? end - 1 : index - 2
      this.tile2Index = index === 0 ? end : index - 1
      this.tile3Index = index
      this.tile4Index = index === end ? 0 : index + 1
      this.tile5Index = index === end - 1 ? 0 : index === end ? 1 : index + 2
    },
    lock() {
      if (this.canlock) {
        this.locked = !this.locked
        this.audio.lock.play()
      }
    }
  }
}
</script>

<style scoped lang="scss">
$tileSize: 90px;
.Reel {
  width: $tileSize;
  height: $tileSize* 2.333;
  overflow: hidden;

  &.is-locked {
    /*   opacity: 0.8; */
    background: rgba(0, 0, 0, 0.1);
  }

  &:not(:last-child) {
    border-right: 1px solid gray(0);
  }
}

.Reel-inner {
  position: relative;
  top: $tileSize * -1 * 1.333;
  display: flex;
  flex-direction: column;
}

.Reel.move .Reel-inner {
  transition: margin-top 0.04s linear;
  margin-top: $tileSize;
}

.Reel-image {
  width: $tileSize;
}

</style>
