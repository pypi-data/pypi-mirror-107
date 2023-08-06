export default {
  data () {
    return {
      float_cached_val: 0.000000,
      float_x_timer: 0,
      float_animate_precision: 0.0001
    }
  },
  mounted () {
    clearInterval(this.float_x_timer)
  },
  destroyed () {
    clearInterval(this.float_x_timer)
  },
  methods: {
    UpdateFunction (currentVal) {

    },
    DoneFunction (end_value) {

    },
    animateValue (oldVal, newValue, duration) {
      const dat = this
      let currentVal = oldVal
      const diff = newValue - oldVal
      const range = diff / dat.float_animate_precision
      const minTime = 50
      const stepTime = Math.max(Math.abs(Math.floor(duration / range)), minTime)
      // console.log("stepTime:,", stepTime);
      const startTime = new Date().getTime()
      const endTime = startTime + duration

      function run () {
        const now = new Date().getTime()
        const remaining = Math.max((endTime - now) / duration, 0)
        const value = newValue - (remaining * diff)
        // console.log("u:,", remaining, value);
        currentVal = value

        try {
          dat.UpdateFunction(currentVal)
        } catch (e) {
          clearInterval(dat.float_x_timer)
        }

        if (value === newValue) {
          dat.float_cached_val = newValue
          clearInterval(dat.float_x_timer)
          dat.DoneFunction(newValue)
        }
      }

      clearInterval(this.float_x_timer)
      this.float_x_timer = setInterval(run, stepTime)
      run()
    }

  }
}
