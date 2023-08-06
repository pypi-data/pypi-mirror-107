// import { WEBSOCKSW, EventBus } from "vue-backgrounds"
// import Ws from "../plugins/iris-ws";
// import getWeb3 from '../plugins/web3js';
// import WsApplication, { RequestBlockHistory } from "../plugins/ws_application";
import Vue from "vue"
import { WEBSOCKSW } from "vue-backgrounds"
import axios from "@/plugins/axios"
import WsMineClient from "@/api/ws/ws_mine"

const state = {
  login_loading: false,
  is_login: false,
  profile_wallet: {},
  profile: {
    cid: "",
    username: "",
    hash: "",
    id: "",
    uid: 0,
    sq: {},
    updatetime: new Date()
  },
  round_game: {
    finalpayout: 0,
    plays: 0,
    amount: 0,
    currency: "",
    level: 0,
    time: "",
    bomb_list: []
  },
  block_history: [],
  game_status: -1,
  up_next: 0,
  waiting_time: 0,
  current_bet_amount: 0,
  current_bet_coin: "--",
  players: [],
  pots: [],
  profile_history: [],
  game_history: [],
  currentBetControls: [],
  last_update_wallet_info: {
    gain: false,
    coin: "---"
  },
  last_update_pot_info: {
    gain: false,
    coin: "---"
  },
  errorproperties: {}

}

const mutations = {
  INIT_MINE_GAME (state, json) {
    WsMineClient.last_update_wallet(state, json.wallet)
    state.profile.username = json.username
    state.profile.hash = json.h
    state.profile.cid = json.wid
    state.game_history = []
    state.profile.updatetime = new Date()
  },
  SINGAL_WALLET (state, payload_wallets) {
    WsMineClient.last_update_wallet(state, payload_wallets)
  },
  FETCH_BLOCK_HISTORY (state, payload) {
    if (state.block_history === null) {
      state.block_history = []
    } else {
      Vue.set(state, "block_history", payload)
    }
  },
  LOGIN_RESULT (state, json) {
    if (json.code === 1) {
      state.is_login = true
      // sync wallet amount, wallet will display as list
      WsMineClient.last_update_wallet(state, json.data.wallet)
    } else {
      state.is_login = false
    }
  },
  CLEAR_PLAYERS (state, json) {
    state.players = []
  },
  MY_CURRENT_BET (state, payload) {
    state.current_bet_amount = payload.amount
    state.current_bet_coin = payload.coin
  },
  UPDATE_BOMB_LIST (state, payload) {
    Vue.set(state.round_game, "bomb_list", payload)
  },
  UPDATE_PAYOUT (state, payload) {
    state.round_game.finalpayout = payload
  },
  ANNOUNCE_GAME_RESULT (state, payload) {
    state.current_bet_amount = payload.amount
  },
  PLAYER_BET_UPDATE (state, o) {
    let found = false
    if (state.players.length > 0) {
      state.players.forEach(function (item, index, array) {
        if (item.i === o.i) {
          //                    state.players[index].c = o.c;
          // user name
          /*       state.players[index].j = o.j;
                 state.players[index].e = o.e;
                 state.players[index].b = o.b;
                 state.players[index].s = o.s;
                 state.players[index].t = o.t; */
          Object.assign(state.players[index], o)
          //  Vue.set (state.players, index, o);
          found = true
        }
      })
      if (!found) {
        state.players.push(o)
      }
    } else {
      state.players.push(o)
    }
  },
  UPDATE_BANK (state, o) {
    let found = false
    const post = o.p[0]
    if (state.pots.length > 0) {
      state.pots.forEach(function (item, index, array) {
        if (String(item.s).toLowerCase() === String(post.s).toLowerCase()) {
          const previous = state.pots[index].locked
          const isgain = parseFloat(post.locked) > parseFloat(previous)
          state.pots[index].s = post.s
          state.pots[index].total = post.total
          state.pots[index].locked = post.locked
          state.pots[index].folks = post.folks
          state.last_update_pot_info.coin = post.s
          state.last_update_pot_info.gain = isgain
          // stop looping
          found = true
        }
      })
      if (!found) {
        state.pots.push(post)
      }
    } else {
      state.pots.push(post)
    }
  },
  GAME_START (state, o) {
    state.round_game = o
    state.round_game.bomb_list = []
    state.round_game.finalpayout = 0
  }
}
let socket_mine_game = null
const actions = {
  wsInitMineGame (context, payload) {
    if (WEBSOCKSW.active || !process.browser) { return }
    WEBSOCKSW.active = true
    if (!(socket_mine_game instanceof WsMineClient)) {
      socket_mine_game = new WsMineClient(context, payload)
    }
  },
  fetchBlockHistory ({ commit }, payload) {
    return new Promise((resolve, reject) => {
      axios.get("/api/inventory")
        .then(function (response) {
          commit("FETCH_BLOCK_HISTORY", response.data.history)
          resolve(response)
        })
        .catch(function (error) {
          reject(error)
        })
    })
  },
  drawUpdate ({ commit }, payload) {
    switch (payload.message) {
      case "killed":
        commit("UPDATE_PAYOUT", payload.data.payout)
        commit("UPDATE_BOMB_LIST", payload.data.list)
        break
      case "complete":
        commit("UPDATE_PAYOUT", payload.data.payout)
        break
      case "draw":
        commit("UPDATE_PAYOUT", payload.data.payout)
        break
      case "repeat":
        //  state.commit ("UPDATE_PAYOUT", payload.data.payout);
        break
    }
  }
}
const getters = {
  IsMineGameLogin (state) {
    return state.is_login
  },
  MinePots (state) {
    return state.pots
  },
  Payout (state) {
    return state.round_game.finalpayout
  },
  MineGameBasicInfo (state) {
    return state.round_game
  },
  MineBlockHistory (state) {
    return state.block_history
  },
  LastBlockResult (state) {
    return state.block_history[0]
  },
  QueryFirstWalletCoinAmountMine (state) {
    const list = Object.keys(state.profile_wallet)
    if (list.length > 0) {
      const coin = list[0]
      const amount = state.profile_wallet[coin].b
      return amount
    } else {
      return 0.0
    }
  },
  QueryFirstWalletSymbolMineGame (state) {
    const list = filter_zerobalance_symbol(state.profile_wallet)
    if (list.length > 0) {
      return list[0]
    } else {
      return "---"
    }
  }
}

function filter_zerobalance_symbol (list) {
  const list_out = []
  const lst = Object.keys(list)
  for (let i = 0; i < lst.length; i++) {
    const symbol = lst[i]
    if (list[symbol].hasOwnProperty("b")) {
      if (list[symbol].b > 0) {
        list_out.push(symbol)
      }
    }
  }
  return list_out
}

function filter_zerobalance (list) {
  const list_out = []
  const lst = Object.keys(list)
  for (let i = 0; i < lst.length; i++) {
    const symbol = lst[i]
    if (list[symbol].hasOwnProperty("b")) {
      if (list[symbol].b > 0) {
        list_out.push(list[symbol])
      }
    }
  }
  return list_out
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
