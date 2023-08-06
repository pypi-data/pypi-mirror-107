const state = {
  login_loading: false,
  is_login: false,
  user_id: 0,
  my_player_id: 0,
  map_my_cash: 0,
  map_players: []
}

const actions = {
  updateCashLine ({ state, commit }, val) {
    commit("coin_amount", val)
  },
  myUserId ({ state, commit }, val) {
    commit("set_player_id", val)
  }
}

const mutations = {
  coin_amount (state, val) {
    const found = state.map_players.findIndex(function (item) {
      return item.userId === val.userId
    })

    if (found === -1) {
      state.map_players.push(val)
    } else {
      state.map_players[found].cash = val.cash
    }
  },
  set_player_id (state, val) {
    state.my_player_id = val
  }
}

const getters = {
  getuserid (state) {
    return state.user_id
  },
  get_cash_value (state) {
    const found = state.map_players.findIndex(function (item) {
      return item.userId === state.my_player_id
    })
    if (found === -1) {
      return 0
    } else {
      return state.map_players[found].cash
    }
  },
  getWalletCoin (state) {
    return function (coin_name) {
      /**
       * coin, amount, locked
       * {c, b, l}
       */
      return state.profile_wallet.find(coin_payload => String(coin_payload.c).toLowerCase() === String(coin_name).toLowerCase())
    }
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
