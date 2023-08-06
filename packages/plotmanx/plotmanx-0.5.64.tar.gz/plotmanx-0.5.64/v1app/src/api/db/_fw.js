import axios from "@/plugins/axios"
import { web3utils } from "@/plugins/staticweb3"
// import qs from "qs";
const UplineCodeBasic = "00FD53"
// const hocoaast = "http://45.77.215.36:8810";
const API_CHECK_AX = "/api/shxconfirm"
const API_CHECK_CH = "/api/checkin"
const state = {
  totalMoney: 0,
  totalCount: 0,
  beginTime: 0,
  levels: 0,
  line_amount: "",
  free_amount: "",
  freeze_amount: "",
  invite_amount: "",
  bonus_amount: "",
  lines_level: "",
  status: 0,
  day_invite_amount: "",
  day_bonus_amount: "",
  invite_code: "",
  be_invited_code: UplineCodeBasic,
  level: 0,
  bal: 0,
  invLen: 0,
  cIndex: 0,
  bLock: 0,
  invitationCode: "",
  user_account: "",
  tokenlist: {},
  tokenFlatList: [],
  islogin: true,
  show_balance: true
}

function showEthVal (th) {
  try {
    const num = web3utils.fromWei(th, "ether")
    console.log("get number: ", num)
    return parseFloat(num)
  } catch (e) {
    return 0
  }
}

const mutations = {
  USER_ACCOUNT_INIT (state, payload) {
    // store web3 user account
    state.user_account = payload
    state.islogin = true
  },
  TOGGLE_SHOE (state, n) {
    state.show_balance = n
  },
  VALUABLES (state, { _totalMoney, _totalCount, _beginTime }) {
    // store web3 user account
    state.totalMoney = _totalMoney
    state.totalCount = _totalCount
    state.beginTime = _beginTime
  },
  T_VALUES (state, { invest_len, curr_index, locked }) {
    state.invLen = parseInt(invest_len)
    state.cIndex = parseInt(curr_index)
    state.bLock = parseInt(locked)
  },
  ETH_BAL (state, payload) {
    // store web3 user account
    state.bal = payload
  },
  PLAYER_DATA (state, { line_amount, free_amount, freeze_amount, invite_amount, bonus_amount, lines_level, status, day_invite_amount, day_bonus_amount, invite_code, be_invited_code, level }) {
    state.line_amount = line_amount
    state.free_amount = free_amount
    state.freeze_amount = freeze_amount
    state.invite_amount = invite_amount
    state.bonus_amount = bonus_amount
    state.lines_level = lines_level
    state.status = status
    state.day_invite_amount = day_invite_amount
    state.day_bonus_amount = day_bonus_amount
    /*  if (invite_code !== "") {
      state.invite_code = invite_code;
    }
    if (be_invited_code === "") {
      state.be_invited_code = UplineCodeBasic;
    } else {
      state.be_invited_code = be_invited_code;
    } */
    state.level = level
  },
  GENERATE_INVITE_CODE (state, code_invitation) {
    state.invitationCode = code_invitation
  },
  GENERATE_UPLINE_CODE (state, code_invitation) {
    state.be_invited_code = code_invitation
  }
}

const actions = {
  admin_checking ({ commit }, payload) {
    commit("VALUABLES", payload)
  },
  admin_test ({ commit }, payload) {
    commit("T_VALUES", payload)
  },
  gen_code ({ commit }, payload) {
    commit("GENERATE_INVITE_CODE", payload)
  },
  gen_upline ({ commit }, payload) {
    commit("GENERATE_UPLINE_CODE", payload)
  },
  user_info ({ commit }, payload) {
    // state.levels = _level;
    commit("PLAYER_DATA", payload)
  },
  isShowBalance ({ commit }, boool) {
    commit("TOGGLE_SHOE", boool)
  }
}

const getters = {
  getShowBalanceAllow (state) {
    return state.show_balance
  },
  isLoginWeb3 (state) {
    return state.islogin
  },
  mycode (state) {
    return state.invitationCode
  },
  upline (state) {
    return state.be_invited_code
  },
  lineCountTimes (state) {
    return state.lineCountTimes
  },
  daily_count (state) {
    return state.day_invite_amount
  },
  totalCount (state) {
    return state.totalCount
  },
  totalMoney (state) {
    return state.totalMoney
  },
  invite_amount (state) {
    return state.invite_amount
  },
  levels (state) {
    return state.levels
  },
  ethwei (state) {
    return showEthVal(state.ethwei)
  },
  principalAmount (state) {
    return showEthVal(state.line_amount) + showEthVal(state.free_amount)
  },
  allIncomeAmount (state) {
    return showEthVal(state.invite_amount) + showEthVal(state.bonus_amount)
  },
  dividendAmount (state) {
    return showEthVal(state.bonus_amount)
  },
  recommendAmount (state) {
    return showEthVal(state.invite_amount)
  },
  waitToSend (state) {
    return showEthVal(state.day_invite_amount) + showEthVal(state.day_bonus_amount)
  },
  lineAmount (state) {
    return showEthVal(state.line_amount)
  },
  lockedAmount (state) {
    return showEthVal(state.freeze_amount)
  },
  level (state) {
    // 5 - level
    return state.lines_level
  },
  inLevel (state) {
    // 11 - inlevel
    return state.level
  },
  valiableAmount (state) {
    return showEthVal(state.free_amount) + showEthVal(state.line_amount)
  },
  haveInAmount (state) {
    return showEthVal(state.freeze_amount) + showEthVal(state.line_amount)
  },
  ready_for_withdrawal (state) {
    return showEthVal(state.free_amount)
  },
  investLen (state) {
    return parseInt(state.invLen)
  },
  cIndex (state) {
    return parseInt(state.cIndex)
  },
  eLock (state) {
    return parseInt(state.bLock)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
