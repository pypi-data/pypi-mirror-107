import { EventBus } from "vue-backgrounds"

export default {
  data () {
    return {
      cached_number: 99999,
      counter_x_timer: 0
    }
  },

  mounted () {
    const dat = this
    EventBus.$on("initsub", dat.update_kj_result)
    EventBus.$on("ingamekj", () => {
      dat.$nextTick(() => {
        dat.update_kj_result()
      })
    })
    dat.$nextTick(() => {
      clearInterval(dat.counter_x_timer)
    })
  },
  destroyed () {
    EventBus.$off("initsub", this.update_kj_result)
    EventBus.$off("ingamekj", this.update_kj_result)
    clearInterval(this.counter_x_timer)
  },

  computed: {
    newNum: {
      get () {
        return this.$store.state.kaijiang.kj_result_n
      },
      set (newValue) {
      }
    },
    last_kj_id: {
      get () {
        return this.$store.state.kaijiang.kj_period_n
      }
    },
    count_down: {
      get () {
        return this.$store.state.kaijiang.count_down
      }
    },
    status: {
      get () {
        return this.$store.state.kaijiang.status
      }
    }
  },
  methods: {

    animateDone (a) {
      console.log("unimplemented animation done.", a)
    },

    animateByNewNumber (new_value) {
      console.log("unimplemented animation done.", new_value)
    },

    getSecondsLeft () {
      return this.count_down
    },
    getKjID () {
      return this.last_kj_id
    },
    getGameStatus () {
      return this.status
    },
    update_kj_result () {
      // console.log ("prize update now...", this.newNum);
      const a = this.newNum.join(""); const dat = this
      const end_numbe = parseInt(a)
      dat.animateValue(this.cached_number, end_numbe, 9000,
        (s) => {
          try {
            dat.animateByNewNumber(s)
          } catch (e) {
            clearInterval(dat.counter_x_timer)
            // console.log ("ex stop...");
          }
        },
        () => {
          dat.cached_number = end_numbe
          dat.animateDone(end_numbe)
        })
    },
    animateValue (oldVal, newValue, duration, funcUpdate, funcDone) {
      let currentVal = oldVal
      const diff = newValue - oldVal
      const range = diff
      const minTime = 50
      const stepTime = Math.max(Math.abs(Math.floor(duration / range)), minTime)
      // console.log("stepTime:,", stepTime);
      const startTime = new Date().getTime()
      const endTime = startTime + duration

      const dat = this

      function run () {
        const now = new Date().getTime()
        const remaining = Math.max((endTime - now) / duration, 0)
        const value = newValue - (remaining * diff)
        // console.log("u:,", remaining, value);
        currentVal = Math.floor(value)
        funcUpdate(currentVal)
        if (value === newValue) {
          clearInterval(dat.counter_x_timer)
          if (funcDone !== undefined) { funcDone() }
        }
      }

      clearInterval(this.counter_x_timer)
      this.counter_x_timer = setInterval(run, stepTime)
      // run ()
    }
  }
}
