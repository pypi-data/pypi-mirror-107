import Vuex from "vuex"
import Vue from "vue"

import walletVuex from "vue-tronlink/src/datavuex/tron"
import trc795 from "../api/db/_trc795"
import trc757 from "../api/db/_trc757"
import trc770 from "../api/db/_trc770"

const createStore = function () {
  const storex = new Vuex.Store({})
  const opts = {}
  storex.registerModule("keno", trc770, opts)
  storex.registerModule("roulette", trc757, opts)
  storex.registerModule("forsage", trc795, opts)
  storex.registerModule("wallet", walletVuex, opts)
  return storex
}

Vue.use(Vuex)
export default createStore
