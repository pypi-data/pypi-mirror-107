const state = {
  g_picked: [],
  g_round_total_income: 0,
  g_total_players: 0,
  g_round_num: 0,
  g_last_draw: 0,
  g_remain_time_block: 0,
  g_min_players_play: 0,
  g_min_bet_draw: 0,
  g_min_players: 0,
  g_sold_ticket_id: 0,
  input_invitation_code: "",
  invite_code: "",
  be_invited_code: "",
  flag_bet_lock: false,
  flag_valid_draw: false,
  flag_valid_purchase: false
}

const getters = {
  saved_picks(state) {
    return state.g_picked
  },
  flags_state(state) {
    return {
      betlock: !!state.flag_bet_lock,
      draw: !!state.flag_valid_draw,
      purchase: !!state.flag_valid_purchase
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
  r(state) {
    return state.g_round_num
  },
  tktid(state) {
    return state.g_sold_ticket_id
  },
  remain_t(state) {
    return state.g_remain_time_block
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
  ylo_address({ commit }, address) {
    commit("PLAYBADDRSS", address)
  },
  ylo_player_matrix({ commit }, bool) {
    commit("PLAYBET", bool)
  },
  ylo_start_flag({ commit }, bool) {
    commit("PLAYSYS", bool)
  },
  lotto_picks({ commit }, picked) {
    commit("LOPICKS", picked)
  },
  /**
   *
   lottoInfo[0] = totalPrizeThisRound;
   lottoInfo[1] = numberOfPlayersThisRound;
   lottoInfo[2] = currentRoundNumber;
   lottoInfo[3] = lastDrawTime;
   lottoInfo[4] = remainTime();
   lottoInfo[5] = minimumToPlay;
   lottoInfo[6] = minimumToDraw;
   lottoInfo[7] = minimumPlayers;
   lottoInfo[8] = ticket_id;
   lottoInfo[9] = 0;
   lottoInfo[10] = 0;
   lottoInfo[11] = 0;
   lottoInfo[12] = 0;
   early_birds = earlyBirdList();

   flags[0] = lockBets;
   flags[1] = validDrawTime();
   flags[2] = validPurchase();
   flags[3] = false;

   * @param commit
   * @param wallet
   * @param hash
   * @param hFlags
   * @param mcInfo
   */
  shenzhen({ commit }, { early_birds, flags, lottoInfo }) {
    commit("SYSINFO", lottoInfo)
    commit("FLAGS", flags)
    commit("PLAYER_DATA", early_birds)
  },
  record_last({ commit }, payload) {
    commit("LAST_BET", payload)
  }
}

const mutations = {
  /**
   flags[0] = lockBets;
   flags[1] = validDrawTime();
   flags[2] = validPurchase();
   flags[3] = false;
   * @param state
   * @param data
   * @constructor
   */
  FLAGS(state, data) {
    state.flag_bet_lock = data[0]
    state.flag_valid_draw = data[1]
    state.flag_valid_purchase = data[2]
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
  },
  /**
   *
   lottoInfo[0] = totalPrizeThisRound;
   lottoInfo[1] = numberOfPlayersThisRound;
   lottoInfo[2] = currentRoundNumber;
   lottoInfo[3] = lastDrawTime;
   lottoInfo[4] = remainTime();
   lottoInfo[5] = minimumToPlay;
   lottoInfo[6] = minimumToDraw;
   lottoInfo[7] = minimumPlayers;
   lottoInfo[8] = ticket_id;
   lottoInfo[9] = 0;
   lottoInfo[10] = 0;
   lottoInfo[11] = 0;
   lottoInfo[12] = 0;
   *
   * @param state
   * @param data
   * @constructor
   */
  SYSINFO(state, data) {
    state.g_round_total_income = data[0]
    state.g_total_players = data[1]
    state.g_round_num = data[2]
    state.g_last_draw = data[3]
    state.g_remain_time_block = data[4]
    state.g_min_players_play = data[5]
    state.g_min_bet_draw = data[6]
    state.g_min_players = data[7]
    state.g_sold_ticket_id = data[8]
    //= =====
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
  PLAYBADDRSS(state, s) {
    state.input_invitation_code = s
  },
  LOPICKS(state, s) {
    state.g_picked = s
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
