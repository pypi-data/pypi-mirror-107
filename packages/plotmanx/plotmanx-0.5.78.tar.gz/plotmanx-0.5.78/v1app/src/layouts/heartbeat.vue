<template>
  <div>
    <nuxt/>
  </div>
</template>

<script>
import { EventBus } from "vue-backgrounds"

/**
 * hb-save-battery - update blockchain data in 20 seconds
 * hb-high-precision - update blockchain data in 2 seconds
 * hb-normal - update blockchain data in 9 seconds
 * hb-custom - allow custom update internals
 */
export default {
  name: "Heartbeat",
  data() {
    return {
      heartbeat: false,
      heartbeatrate: 9000
    }
  },
  mounted() {
    this.$nextTick(() => {
      if (!this.heartbeat) {
        this.heartbeat = setInterval(() => {
          EventBus.$emit("heartbeat")
        }, this.heartbeatrate)
        EventBus.$emit("heartbeat")
      }
      EventBus.$on("hb-save-battery", () => {
        this.heartbeatrate = 20000
      })
      EventBus.$on("hb-high-precision", () => {
        this.heartbeatrate = 2000
      })
      EventBus.$on("hb-normal", () => {
        this.heartbeatrate = 9000
      })
      EventBus.$on("hb-custom", (musecond) => {
        if (typeof musecond === "number") {
          this.heartbeatrate = musecond
        }
      })
    })
  }
}
</script>

<style scoped lang="scss">
html {
  font-family: "Source Sans Pro", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  font-size: 16px;
  word-spacing: 1px;
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  box-sizing: border-box;
}

*, *:before, *:after {
  box-sizing: border-box;
  margin: 0;
}
</style>
