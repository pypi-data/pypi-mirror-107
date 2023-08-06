import string_tx from "@/api/mixins/string_tx"
import wxall from "@/api/mixins/tron/walletx"
import { txtUnitRomanize } from "@/api/compress/bn"

export default {
  mixins: [wxall, string_tx],
  data() {
    return {
      cells: []
    }
  },
  methods: {
    setup_levels() {
      if (this.cells.length === 0) {
        for (let i = 1; i <= 12; i++) {
          this.cells.push(
            {
              key: `lvl-${i}`,
              title: txtUnitRomanize(i),
              amount: "1000",
              blocked_x3: false,
              blocked_x6: false,
              currency: "TRX"
            }
          )
        }
      }
    },
    update_price_plan() {
      const list = this.loadLocal("forsage/show_price_plan")
      if (list.length > 0) {
        list.forEach((numberX, index) => {
          const result = this.fromSun(numberX)
          this.cells[index].amount = String(result)
        })
      }
    },
    check_lvl_plan() {
      const map = this.loadLocal("forsage/show_lvl_map")
      for (let i = 0; i < 12; i++) {
        // this[`_lvl_map_${i}_x3`] = map.get(i)[0]
        // this[`_lvl_map_${i}_x6`] = map.get(i)[1]
        if (map.get(i) === undefined || typeof map.get(i) !== "object") {
          continue
        }
        this.cells[i].blocked_x3 = map.get(i)[0]
        this.cells[i].blocked_x6 = map.get(i)[1]
      }
    }
  }
}
