export default {
  methods: {
    getComs () {
      return []
    },
    get10s (n) {
      return Math.floor(n / 10)
    },
    get100s (n) {
      return Math.floor(n / 100)
    },
    get1000s (n) {
      return Math.floor(n / 1000)
    },
    get10000s (n) {
      return Math.floor(n / 10000)
    },
    getShowNum (numba) {
      if (typeof numba !== "number") { return }
      if (numba < 10) {
        this.getComs()[0].updateNumber(0)
        this.getComs()[1].updateNumber(0)
        this.getComs()[2].updateNumber(0)
        this.getComs()[3].updateNumber(0)
        this.getComs()[4].updateNumber(numba % 10)
        return
      }
      if (numba < 100) {
        this.getComs()[0].updateNumber(0)
        this.getComs()[1].updateNumber(0)
        this.getComs()[2].updateNumber(0)
        this.getComs()[3].updateNumber(this.get10s(numba))
        this.getComs()[4].updateNumber(numba % 10)
        return
      }
      if (numba < 1000) {
        this.getComs()[0].updateNumber(0)
        this.getComs()[1].updateNumber(0)
        this.getComs()[2].updateNumber(this.get100s(numba))
        this.getComs()[3].updateNumber(this.get10s(numba))
        this.getComs()[4].updateNumber(numba % 10)
        return
      }
      if (numba < 10000) {
        this.getComs()[0].updateNumber(0)
        this.getComs()[1].updateNumber(this.get1000s(numba))
        this.getComs()[2].updateNumber(this.get100s(numba))
        this.getComs()[3].updateNumber(this.get10s(numba))
        this.getComs()[4].updateNumber(numba % 10)
        return
      }
      if (numba < 100000) {
        this.getComs()[0].updateNumber(this.get10000s(numba))
        this.getComs()[1].updateNumber(this.get1000s(numba))
        this.getComs()[2].updateNumber(this.get100s(numba))
        this.getComs()[3].updateNumber(this.get10s(numba))
        this.getComs()[4].updateNumber(numba % 10)
      }
    }
  }
}
