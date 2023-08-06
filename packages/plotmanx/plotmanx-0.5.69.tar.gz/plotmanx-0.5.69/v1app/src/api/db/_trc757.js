const state = {
  user_bet_on: 0,
  bank_secret: 0,
  user_value: 0,
  locked_fund: 0,
  time_stamp_secret_post: 0,
  time_stamp_last_play: 0,
  available_fund_to_bet: 0,
  bank_hash: "",
  g_timeout: 0,
  g_inplay: false,
  g_subbet: false,
  g_roulette_number: 0,
  g_management_fee: 0,
  g_banker_fund: 0,
  g_banker_locked_fund: 0,
  g_time_now: 0,
  g_last_game_result_tx: -1,
  g_go_confirm_block: -1,
  flag_value_ready: false,
  flag_hash_ready: false,
  flag_game_requested: false
}

const getters = {
  flags_interpret(state) {
    return {
      value: !!state.flag_value_ready,
      hash: !!state.flag_hash_ready,
      requested: !!state.flag_game_requested
    }
  },
  yf_flags(state) {
    return {
      play: state.g_inplay,
      bet_sub: state.g_subbet
    }
  },
  user_bet_on(state) {
    return state.user_bet_on
  },
  bank_secret(state) {
    return state.bank_secret
  },
  user_value(state) {
    return state.user_value
  },
  locked_fund(state) {
    return state.locked_fund
  },
  bank_hash(state) {
    return state.bank_hash
  },
  pocket_fund(state) {
    return state.available_fund_to_bet
  },
  g_timeout(state) {
    return state.g_timeout
  },
  g_roulette_number(state) {
    return state.g_roulette_number
  },
  g_management_fee(state) {
    return state.g_management_fee
  },
  g_banker_fund(state) {
    return state.g_banker_fund
  },
  g_banker_locked_fund(state) {
    return state.g_banker_locked_fund
  },
  block_time_last_update(state) {
    return state.g_time_now
  },
  time_post_secret(state) {
    return state.time_stamp_secret_post
  },
  time_last_play(state) {
    return state.time_stamp_last_play
  },
  gg_result(state) {
    return state.g_last_game_result_tx
  },
  gg_block(state) {
    return state.g_go_confirm_block
  }
}

const actions = {
  yf_bet_sub({ commit }, bool) {
    commit("PLAYBET", bool)
  },
  yf_start_flag({ commit }, bool) {
    commit("PLAYSYS", bool)
  },
  shenzhen({ commit }, { wallet, hash, hFlags, mcInfo }) {
    commit("SYSINFO", mcInfo)
    commit("FLAGS", hFlags)
    commit("PLAYER_DATA", wallet)
    commit("UPDATE_HASH", hash)
  },
  record_last({ commit }, payload) {
    commit("LAST_BET", payload)
  }
}

const mutations = {
  /**
   * this is the flags of commands
   **/
  FLAGS(state, data) {
    state.flag_value_ready = data[0]
    state.flag_hash_ready = data[1]
    state.flag_game_requested = data[2]
  },
  /**
   * the standard way to keep all the player data
   *
   GameRound memory check = gameRounds[target];
   wallet[0] = check.hasUserBetOnRed ? 1 : 0;
   wallet[1] = check.bankSecretValue;
   wallet[2] = check.userValue;
   wallet[3] = check.lockedFunds;
   wallet[4] = check.timeWhenSecretUserValueSubmitted;
   wallet[5] = userFund(_msgSender());
   wallet[6] = hasRequestedGame[target] ? 1 : 0;
   wallet[7] = check.lastGamePlayTime;
   *
   * @param state
   * @param use_load
   * @constructor
   */
  PLAYER_DATA(state, use_load) {
    state.user_bet_on = use_load[0]
    state.bank_secret = use_load[2]
    state.user_value = use_load[1]
    state.locked_fund = use_load[3]
    state.time_stamp_secret_post = use_load[4]
    state.available_fund_to_bet = use_load[5]
    state.time_stamp_last_play = use_load[7]
  },
  /**
   *
   sysInfo[0] = TIMEOUT_FOR_BANK_REVEAL;
   sysInfo[1] = ROULETTE_NUMBER_COUNT;
   sysInfo[2] = managementFeePool;
   sysInfo[3] = bankerFund();
   sysInfo[4] = gameRounds[bankAddress].lockedFunds;
   sysInfo[5] = now;
   *
   * @param state
   * @param data
   * @constructor
   */
  SYSINFO(state, data) {
    state.g_timeout = data[0]
    state.g_roulette_number = data[1]
    state.g_management_fee = data[2]
    state.g_banker_fund = data[3]
    state.g_banker_locked_fund = data[4]
    state.g_time_now = data[5]
  },
  UPDATE_HASH(state, s) {
    state.bank_hash = s
  },

  PLAYSYS(state, s) {
    state.g_inplay = s
  },
  PLAYBET(state, s) {
    state.g_subbet = s
  },
  LAST_BET(state, { transaction, block }) {
    state.g_last_game_result_tx = transaction
    state.g_go_confirm_block = block
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
