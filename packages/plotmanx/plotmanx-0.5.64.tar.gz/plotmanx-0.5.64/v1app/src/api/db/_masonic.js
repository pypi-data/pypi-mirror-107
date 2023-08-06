import axios from "@/plugins/axios"
import { sum } from "@/api/compress/bn"

const API_CHECK_AX = "/api/shxconfirm"
const API_CHECK_CH = "/api/checkin"
const state = {
  g_currentRound: 0,
  g_uid: 0,
  g_startTime: 0,
  g_totalCount: 0,
  g_totalMoney: 0,
  g_sumRound: 0,
  g_bonusLimit: 0,
  g_sendLimit: 0,
  g_drawLimit: 0,
  g_canimport: 0,
  g_lineStatus: 0,
  g_lineLen: 0,
  g_canSetStartTime: 0,
  g_manson: 0,
  now_time: 0,
  user_id: "",
  line_amount: 0,
  free_amount: 0,
  freeze_amount: 0,
  invite_amount: 0,
  bonus_amount: 0,
  key_amount: 0,
  lines_level: 0,
  day_invite_amount: 0,
  day_bonus_amount: 0,
  mined_amount: 0,
  investTimes: 0,
  node_count: 0,
  last_invest_time: "",
  status: 0,
  reward_index: "",
  level: 0,
  bal: 0,
  invLen: 0,
  bLock: 0,
  bMaxPrincipal: 0,
  sell_price: 0,
  exchange_status: 0,
  input_invitation_code: "",
  invite_code: "",
  be_invited_code: "",
  user_account: "",
  tokenlist: {},
  tokenFlatList: [],
  price_plans: [],
  user_ingame: false,
  islogin: true,
  show_balance: true,
  game_started: false
}

const mutations = {
  /**
   * user account save data in here
   * @param state
   * @param payload
   * @constructor
   */
  USER_ACCOUNT_INIT(state, payload) {
    // store web3 user account
    state.user_account = payload
    state.islogin = true
  },
  /**
   * toggle the shoes
   * @param state
   * @param n
   * @constructor
   */
  TOGGLE_SHOE(state, n) {
    state.show_balance = n
  },
  /**
   * the standard shenzhen values from the system solidity
   * @param state
   * @param shenzhen_info
   * @constructor
   */
  SYSTEM_VALUE_SHENZHEN(state, shenzhen_info) {
    state.g_currentRound = shenzhen_info[0]
    state.g_uid = shenzhen_info[1]
    state.g_startTime = shenzhen_info[2]
    state.g_totalCount = shenzhen_info[3]
    state.g_totalMoney = shenzhen_info[4]
    state.g_sumRound = shenzhen_info[5]
    state.g_bonusLimit = shenzhen_info[6]
    state.g_sendLimit = shenzhen_info[7]
    state.g_drawLimit = shenzhen_info[8]
    state.g_canimport = shenzhen_info[9]
    state.g_lineStatus = shenzhen_info[10]
    state.g_lineLen = shenzhen_info[11]
    state.g_canSetStartTime = shenzhen_info[12]
    state.g_manson = shenzhen_info[13]
  },
  /**
   * the standard way to keep all the player data
   * @param state
   * @param use_load
   * @constructor
   */
  PLAYER_DATA(state, use_load) {
    state.line_amount = use_load[1]
    state.free_amount = use_load[2]
    state.freeze_amount = use_load[3]
    state.invite_amount = use_load[4]
    state.bonus_amount = use_load[5]
    state.key_amount = use_load[6]
    state.lines_level = use_load[7]
    state.day_bonus_amount = use_load[8]
    state.reward_index = use_load[9]
    state.investTimes = use_load[10]
    state.level = use_load[11]
    state.mined_amount = use_load[12]
    state.last_invest_time = use_load[13]
    state.status = use_load[14]
    state.sell_price = use_load[15]
    state.exchange_status = use_load[16]
  },
  ETH_BAL(state, payload) {
    // store web3 user account
    state.bal = payload
  },
  USER_CODE_NON(state, result_ingame) {
    state.user_ingame = result_ingame
  },
  USER_CODE_REGISTRATION(state, {
    upline_code,
    invite_code
  }) {
    state.invite_code = invite_code
    state.be_invited_code = upline_code
  },
  UPDATE_NOW(state, dat_time) {
    state.now_time = dat_time
  },
  GENERATE_INVITE_CODE(state, code_invitation) {
    state.input_invitation_code = code_invitation
  },
  ENTER_UPLINE_CODE(state, code_invitation) {
    state.be_invited_code = code_invitation
  },
  EXTRA_ACCOUNT_DATA(state, results) {
    state.node_count = results.nodecount
  },
  MY_CAPACITY_TRX(state, value) {
    state.bMaxPrincipal = value
  },
  CAN_VEGAS(state, value) {
    state.game_started = value
  },
  PRICE_PLAN_INFO(state, data_list) {
    state.price_plans = data_list
  }
}
const player_x = {
  invite_amount(state) {
    return state.invite_amount
  },
  myHackedKeyAmount(state) {
    return state.key_amount
  },
  /**
   * the free amount that is ready to take out
   * @param state
   * @returns {number | undefined}
   */
  ready_for_withdrawal(state) {
    return String(state.free_amount)
  },
  /**
   * total amount of trx is stored in the contract
   * + the free amount
   * + waiting entrance amount
   * + the freezed amount
   * @param state
   * @returns {number}
   */
  principalAmount(state) {
    return String(sum([
      state.line_amount,
      state.free_amount,
      state.freeze_amount
    ]))
  },
  allIncomeAmount(state) {
    return String(sum([
      state.invite_amount,
      state.bonus_amount
    ]))
  },
  dividendAmount(state) {
    return String(state.bonus_amount)
  },
  recommendAmount(state) {
    return String(state.invite_amount)
  },
  waitToSend(state) {
    return String(state.mined_amount)
  },
  lineAmount(state) {
    return String(state.line_amount)
  },
  lockedAmount(state) {
    return String(state.freeze_amount)
  },
  line_level(state) {
    // 5 - level
    return state.lines_level
  },
  freeze_level(state) {
    // 11 - inlevel
    return state.level
  },
  valiableAmount(state) {
    return String(sum([
      state.free_amount,
      state.line_amount
    ]))
  },
  haveInAmount(state) {
    return String(sum([
      state.freeze_amount,
      state.line_amount
    ]))
  },
  investLen(state) {
    return parseInt(state.invLen)
  },
  nodeCount(state) {
    return state.node_count
  },
  registered_user(state) {
    return !!state.user_ingame
  },
  mycode(state) {
    return state.input_invitation_code
  },

  daily_count(state) {
    return state.day_invite_amount
  },
  _max(state) {
    return state.bMaxPrincipal
  }
}
const actions = {

  inmax({ commit }, payload) {
    commit("MY_CAPACITY_TRX", payload)
  },
  shenzhen({ commit }, payload) {
    commit("SYSTEM_VALUE_SHENZHEN", payload)
  },
  gen_code({ commit }, payload) {
    commit("GENERATE_INVITE_CODE", payload)
  },
  enter_upline({ commit }, code) {
    commit("ENTER_UPLINE_CODE", code)
  },
  price_entry_info({ commit }, payload) {
    commit("PRICE_PLAN_INFO", payload)
  },
  can_vegas({ commit }, payload) {
    commit("CAN_VEGAS", payload)
  },
  player_ingame({ commit }, payload) {
    commit("USER_CODE_NON", payload)
  },
  user_info({ commit }, payload) {
    const upline_code = payload.deViciCode
    const invite_code = payload.inviteCode
    const user_info = payload.info
    if (upline_code.length > 0 && invite_code.length > 0) {
      commit("USER_CODE_REGISTRATION", {
        upline_code,
        invite_code
      })
    }
    commit("PLAYER_DATA", user_info)
  },
  isShowBalance({ commit }, bool) {
    commit("TOGGLE_SHOE", bool)
  },
  // eslint-disable-next-line require-await
  async demo_sync({ commit, state }, payload_demo) {
    //  payload.from = my_wallet_address;
    //  return axios.post (API_CHECK_AX, qs.stringify (payload_demo))
    return axios.post(API_CHECK_AX, payload_demo)
      .then((response) => {
        console.log("server demo_sync", response.data)
      })
      .catch((error) => {
        console.log("post er::", error)
      })
  },
  // eslint-disable-next-line require-await
  async before_confirmed_check({ commit }, payload) {
    return axios.post(API_CHECK_AX, payload)
      .then((response) => {
        // that.$store.dispatch ("blockhistory_init", response.data.list);
        // commit ("append_block_history_php", response.data.list)
        console.log("server before_confirmed_check", response.data)
      })
      .catch(() => {
        // console.log ("post er::", error)
      })
  },
  // eslint-disable-next-line require-await
  async checkAccountData({ commit, state }, payload) {
    return axios.post(API_CHECK_CH, payload)
      .then((response) => {
        console.log("server checkAccountData", response.data)
        const result = response.data.result
        commit("EXTRA_ACCOUNT_DATA", result)
      })
      .catch(() => {
        // console.log ("post er::", error);
        commit("EXTRA_ACCOUNT_DATA", { nodecount: 0 })
      })
  }
}

const getters = {
  ...player_x,
  canVegas(state) {
    return state.game_started
  },
  getShowBalanceAllow(state) {
    return state.show_balance
  },
  isLoginWeb3(state) {
    return state.islogin
  },
  _totalCount(state) {
    return state.g_totalCount
  },
  _totalMoney(state) {
    return String(state.g_totalMoney)
  },
  _prize_pot(state) {
    return String(state.g_manson)
  },
  sameStartInCountDown(state) {
    // the current round start time
    return state.g_startTime - state.now_time
    // how many seconds;
  },
  upline(state) {
    return state.be_invited_code
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
  eLock(state) {
    return parseInt(state.bLock)
  },
  get_price_plan(state) {
    return state.price_plans
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
