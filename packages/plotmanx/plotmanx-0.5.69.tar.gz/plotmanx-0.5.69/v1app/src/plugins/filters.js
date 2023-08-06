// eslint-disable-next-line no-extend-native
import Vue from "vue"
import {
  trx, trxLong, trxUnit, hexUnitFloat,
  txtUnit, FillZero, blocktime, duration,
  txtUnitRomanize
} from "@/api/compress/bn"
// eslint-disable-next-line no-extend-native
Number.prototype.formatCurrency = function (thou = ",", dec = ".", sym = "$") {
  return this.toFixed(2).toString().split(/[-.]/).reverse().reduceRight(function (t, c, i) {
    return (i === 2) ? "-" + t : (i === 1) ? t + c.replace(/(\d)(?=(\d{3})+$)/g, "$1" + thou) : t + dec + c
  }, sym)
}

Vue.filter("trx", trx)
Vue.filter("trxlong", trxLong)
Vue.filter("trxunit", trxUnit)
Vue.filter("hexunitfloat", hexUnitFloat)
Vue.filter("unit", txtUnit)
Vue.filter("unitromance", txtUnitRomanize)
Vue.filter("unixtime", blocktime)
Vue.filter("unixduration", duration)

Vue.filter("fix4", function (value) {
  value = parseFloat(value)
  return Number(value).toFixed(4)
})
Vue.filter("fix3", function (value) {
  value = parseFloat(value)
  return Number(value).toFixed(3)
})
Vue.filter("fix6", function (value) {
  value = parseFloat(value)
  return Number(value).toFixed(6)
})
Vue.filter("uppercase", function (value) {
  return String(value).toUpperCase()
})
Vue.filter("reverse", function (value) {
  return value.split("").reverse().join("")
})
Vue.filter("shorten_hash", function (value) {
  const n = String(value)
  return n.substring(0, 10) + "..." + n.substr(n.length - 10)
})
Vue.filter("shorten_hash_mini", function (value) {
  const n = String(value)
  return n.substring(0, 5) + "..." + n.substr(n.length - 5)
})
Vue.filter("fill_zero_5", function (value) {
  return FillZero(value, 5)
})
Vue.filter("notification_code", function (value) {
  if (value === 0) {
    return ""
  } else {
    return String(value)
  }
})
Vue.filter("changeprofit", function (value) {
  value = parseFloat(value)
  if (value > 0) {
    return "+" + Number(value).toFixed(4)
  } else {
    return "0.0"
  }
})
Vue.filter("coinName", function (value) {
  return String(value).toUpperCase()
})
Vue.filter("coinbalance", function (value) {
  value = parseFloat(value)
  if (value > 0) {
    return Number(value).formatCurrency(",", ".", "")
  } else {
    return ""
  }
})
Vue.filter("coinbalance_zero", function (value) {
  value = parseFloat(value)
  if (value > 0) {
    return Number(value).formatCurrency(",", ".", "")
  } else {
    return "0.00"
  }
})

Vue.filter("percentage", function (value) {
  value = parseFloat(value)
  const j = (Number(value) * 100).toFixed(4)
  if (j > 0) {
    return j + "%"
  } else {
    return "--"
  }
})
Vue.filter("bet_n", function (value) {
  const j = parseInt(value)
  if (j < 10 && j > 0) {
    return "0" + Number(j)
  } else {
    return j
  }
})
