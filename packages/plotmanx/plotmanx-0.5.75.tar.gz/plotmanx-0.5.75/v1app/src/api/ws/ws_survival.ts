import { EventBus } from "vue-backgrounds/src/engines/EventBus"
import WsBasis from "./wsBase"
// import IrisWsClassic from "../plugins/iris-ws";
import CxSocket from "./cxsock"

export default class WsAppSurvival extends WsBasis {
  constructor({ commit }, int_options) {
    super()
    const socket_ws = new CxSocket("ws://161.117.84.89:2019/ws", null, "iris-websocket-message")
    socket_ws.forceStringMessageType()
    socket_ws.OnConnect(function () {
      /**
       * user basic
       */
      if (typeof int_options === "object") {
        socket_ws.Emit("start", JSON.stringify(int_options))
      } else {
        socket_ws.Emit("start", "")
      }
      console.log("connected now ")
      EventBus.$emit("connected", "back to connected")
    })
    socket_ws.OnDisconnect(function () {
      EventBus.$emit("disconnected", "You are now disconnected. Please refresh.. 你现在离线了。")
    })
    /* socket_ws.On("ping", function (msg) {
      socket_ws.Emit("pong", "");
    }); */
    socket_ws.On("init", function (msg) {
      // console.log("enter commit name init_sock");
      WsBasis.takeCommitOnly(commit, "init_sock", msg)
    })
    socket_ws.On("auth_request", (msg) => {
      console.log("test", msg)
      WsBasis.takeAllChannels(commit, "login_result", "login_result", msg)
    })
    socket_ws.On("pot_update", (msg) => {
      WsBasis.takeAllChannels(commit, "pot_update", "pot_update", msg)
    })

    socket_ws.On("recover_pass", (msg) => {
      WsBasis.takeEventBusOnly(commit, "passwrecovery_response", msg)
    })
    socket_ws.On("recover_verify", (msg) => {
      WsBasis.takeEventBusOnly(commit, "passwrecverif_response", msg)
    })

    /**
     * big bang run ex. specific
     */

    socket_ws.On("player_list_update", (msg) => {
      // socket_ws.Emit ("check_result_transaction_id", JSON.stringify (msg));
    })
    socket_ws.On("escape_request", (msg) => {
      WsBasis.takeEventBusOnly(commit, "escape_request", msg)
      // socket_ws.Emit ("check_result_transaction_id", JSON.stringify (msg));
    })
    socket_ws.On("bet_request", (msg) => {
      WsBasis.takeEventBusOnly(commit, "bet_request", msg)
      // socket_ws.Emit ("check_result_transaction_id", JSON.stringify (msg));
    })
    socket_ws.On("pot_ls_update", (msg) => {
      WsAppSurvival.dedicated_pot_ls(commit, msg)
    })
    socket_ws.On("player_update", (msg) => {
      WsBasis.takeAllChannels(commit, "player_update", "player_update", msg)
    })
    socket_ws.On("snapshot_load", (msg) => {
      WsBasis.takeCommitOnly(commit, "snapshot_load_ec", msg)
    })
    socket_ws.On("bb_status", (msg) => {
      WsBasis.takeEventChildCommitOnly(commit, msg, "bb_extra", "extras")
      WsBasis.takeAllChannels(commit, "bb_status", "bb_status", msg)
    })
    socket_ws.On("profile_update", (msg) => {
      WsAppSurvival.dedicated_profile_update(commit, msg)
    })
    socket_ws.On("bb_tick", (msg) => {
      WsBasis.takeEventBusOnly(commit, "bb_tick", msg)
    })
    WsBasis.EventEmit(socket_ws, "bb_bet", "bet")
    WsBasis.EventEmit(socket_ws, "bb_escape", "escape")
    WsBasis.EventEmit(socket_ws, "login_pass", "auth")
    WsBasis.EventEmit(socket_ws, "join_game", "sub")
    WsBasis.EventEmit(socket_ws, "exit_game", "unsub")
    WsBasis.EventEmit(socket_ws, "request_snapshot_data_packet", "snapshot_load")
    WsBasis.EventEmit(socket_ws, "request_fgpw_send", "recover_pass")
    WsBasis.EventEmit(socket_ws, "request_fgpw_setup", "recover_verify")
  }

  static dedicated_profile_update(commit, msg) {
    if (msg === "") { return }
    try {
      const object_filled = JSON.parse(msg)
      commit("user_wallet_renew", object_filled.wallet)
      commit("bb_profile_update", object_filled)
      // EventBus.$emit ("profile_update", bjson);
      // console.log("profile update xx")
    } catch (e) {
      console.error("server internal error dedicated_profile_update ", e)
    }
  }

  static dedicated_pot_ls(commit, msg) {
    if (msg === "") { return }
    try {
      const object_filled = JSON.parse(msg)
      commit("pot_ls_update", object_filled.p)
      commit("append_block_history", object_filled)
      // console.log ("pot list update xx", object_filled.p)
      // EventBus.$emit ("pot_ls_update_c", object_filled);
    } catch (e) {
      console.error("server internal error dedicated_pot_ls ", e, msg)
    }
  }

  static UpdateWallet(state, wallet_payload) {
    if (typeof wallet_payload !== "object") { return }
    wallet_payload.forEach(function (coin_payload, a, b) {
      if (String(coin_payload.c).trim() === "") { return }
      const coin = String(coin_payload.c).toLowerCase()
      const paylo = {
        b: coin_payload.b,
        l: coin_payload.l,
        c: coin
      }
      if (state.profile_wallet.hasOwnProperty(coin)) {
        state.last_update_wallet_info.coin = coin
        state.last_update_wallet_info.gain = state.profile_wallet[coin].b < coin_payload.b
      }
      // Vue.set(state.profile_wallet, coin, paylo);
      // console.log(globalstate.surivial);
      // const state = globalstate.surivial;
      if (!state.profile_wallet.hasOwnProperty(coin)) {
        state.profile_wallet[coin] = Object.assign({}, paylo)
      } else {
        state.profile_wallet[coin] = Object.assign(state.profile_wallet[coin], paylo)
        /*     state.profile_wallet[coin].c = coin;
             state.profile_wallet[coin].b = coin_payload.b;
             state.profile_wallet[coin].l = coin_payload.l;
        */
      }
    })
  }
}
