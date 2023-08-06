const state = {
  x3referrer: 0,
  x6referrer: 0,
  x3Matrix: "",
  x3Matrix_address: "",
  x3Matrix_address_list: "",
  x3Matrix_blocked: "",
  x6Matrix: "",
  x6Matrix_address: "",
  x6Matrix_1st_list: "",
  x6Matrix_2snd_list: "",
  x6Matrix_blocked: "",
  x3LevelBool: [],
  x6LevelBool: [],
  x3Last: 0,
  x6Last: 0,
  mylvl: new Map(),
  user_ingame: false,
  in_block_process: false,
  input_invitation_code: "",
  invite_code: "",
  be_invited_code: "",
  earning: 0,
  uid: 0,
  partners: 0,
  joined_time: 0,
  _price_plan: [],
  _min_price: 0,
  _last_level: 0,
  _bank: 0,
  _last_user_id: 0,
  _current_time: 0,
  _online_tme: 0
}

const getters = {
  show_in_game(state) {
    return state.user_ingame
  },
  should_generate_invitation_code(state) {
    const a = state.be_invited_code.length === 0
    const b = state.invite_code.length === 0
    if (!state.user_ingame && a && b) {
      return true
    } else {
      return false
    }
  },
  show_invitation_code(state) {
    const a = state.input_invitation_code
    const b = state.invite_code
    const c = state.input_invitation_code.length === 0
    const d = state.invite_code.length === 0
    if (c) {
      return b
    }
    if (d) {
      return a
    }
    return b
  },
  show_upline(state) {
    return state.be_invited_code
  },
  show_earning(state) {
    return state.earning
  },
  show_bank(state) {
    return state._bank
  },
  get_min_start_ticket_price(state) {
    return state._min_price
  },
  show_investors(state) {
    return state._last_user_id
  },
  show_block_in_process(state) {
    return state.in_block_process
  },
  show_price_plan(state) {
    return state._price_plan
  },
  show_lvl_map(state) {
    return state.mylvl
  }
}

const actions = {
  level_price({ commit }, payload) {
    commit("PRICE_LEVELS", payload)
  },
  level_info({ commit }, payload) {
    commit("STORE_USER_LEVELS", payload)
  },
  player_ingame({ commit }, payload) {
    commit("USER_CODE_NON", payload)
  },
  in_block_transaction({ commit }, on) {
    commit("BLOCKTRANSACTION", on)
  },
  store_level({ commit }, dat) {
    commit("MY_LEVEL", dat)
  },
  player_imatrix({ commit }, { maimai, iv, ref }) {
    const upline_code = ref
    const invite_code = iv
    if (upline_code.length > 0 && invite_code.length > 0) {
      commit("USER_CODE_REGISTRATION", {
        upline_code,
        invite_code
      })
      commit("USER_CODE_NON", true)
    } else if (upline_code === "" && invite_code === "VERSA") {
      // for a special user only
      commit("USER_CODE_REGISTRATION", {
        upline_code,
        invite_code
      })
      commit("USER_CODE_NON", true)
    }
    commit("PLAYER_DATA", maimai)
  },
  parisLos({ commit }, { systemInfod }) {
    commit("SYSINFO", systemInfod)
  },
  pinned_code({ commit }, code) {
    commit("ENTER_UPLINE_CODE", code)
  },
  gen_code({ commit }, payload) {
    commit("GENERATE_INVITE_CODE", payload)
  }
}

const mutations = {
  GENERATE_INVITE_CODE(state, code_invitation) {
    state.input_invitation_code = code_invitation
  },
  USER_CODE_REGISTRATION(state, {
    upline_code,
    invite_code
  }) {
    state.invite_code = invite_code
    state.be_invited_code = upline_code
  },
  MY_LEVEL(state, { lv, x3, x6 }) {
    const map = state.mylvl
    map.set(lv, [x3, x6])
    state.mylvl = map
  },
  PRICE_LEVELS(state, { level_max, price_list }) {
    state._last_level = level_max
    state._price_plan = price_list
  },
  STORE_USER_LEVELS(state, { x3Levels, x6Levels, x3LastTrue, x6LastTrue }) {
    // store web3 user account
    state.x3LevelBool = x3Levels
    state.x6LevelBool = x6Levels
    state.x3Last = x3LastTrue
    state.x6Last = x6LastTrue
  },
  USER_CODE_NON(state, result_ingame) {
    state.user_ingame = result_ingame
  },
  BLOCKTRANSACTION(state, transaction) {
    state.in_block_process = transaction
  },
  ENTER_UPLINE_CODE(state, code_invitation) {
    state.be_invited_code = code_invitation
  },
  /**
   * the standard way to keep all the player data
   * @param state
   * @param use_load
   * @constructor
   */
  PLAYER_DATA(state, use_load) {
    state.earning = use_load[0]
    state.uid = use_load[1]
    state.partners = use_load[2]
    state.joined_time = use_load[3]
  },
  SYSINFO(state, loadf) {
    state._min_price = loadf[0]
    state._bank = loadf[2]
    state._last_level = loadf[1]
    state._last_user_id = loadf[3]
    state._current_time = loadf[4]
    state._online_tme = loadf[5]
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
