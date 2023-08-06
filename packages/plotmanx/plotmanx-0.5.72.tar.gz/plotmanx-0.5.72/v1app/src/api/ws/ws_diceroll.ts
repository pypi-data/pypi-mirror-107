import { EventBus } from "vue-backgrounds/src/engines/EventBus"
import WsBasis from "./wsBase"
import CxSocket from "./cxsock"

export default class WsMineClient extends WsBasis {
  constructor({ commit }, int_options) {
    super()

    const socket_ws = new CxSocket("ws://localhost:2025/ws", null, "iris-websocket-message")

    socket_ws.OnConnect(function () {
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
    socket_ws.On("ping", function (msg) {
      socket_ws.Emit("pong", "")
    })
    socket_ws.On("rollin", function (json) {
      WsBasis.takeCommitOnly(commit, "update_game_result_dice", json)
    })
    socket_ws.On("rafflin", function (json) {
      WsBasis.takeCommitOnly(commit, "update_game_result_raffle", json)
    })
    socket_ws.On("rt", function (json) {
      if (json === "") { return }
      const jsb = JSON.parse(json)
      // console.log ("new_roll", jsb);
      //  EventBus.$emit("new_roll", js);
      if (jsb.gid === 1) {
        commit("append_gh1", jsb)
      }
      if (jsb.gid === 2) {
        commit("append_gh2", jsb)
      }
    })
    socket_ws.On("ebzinfo", function (json) {
      WsBasis.takeCommitOnly(commit, "roulette_updates", json)
    })
    socket_ws.On("ebzact", function (json) {
      WsBasis.takeCommitOnly(commit, "roulette_action", json)
    })
    socket_ws.On("ebzl", function (json) {
      WsBasis.takeCommitOnly(commit, "roulette_players", json)
    })
    socket_ws.On("ebz", function (json) {
      /**
       {
       "detail":{
       "name":"ETH.main",
       "height":6341576,
       "hash":"1490f4d4bd986e6276cf7d2154ab95dbdd18ef53b121507552dad5c89d10c5b8",
       "time":"2018-09-16T09:54:48.495296689Z",
       "previous_hash":"00b32c0b73b65d21e441bb5e6e527bc46f71f4995241e8c60b042bb0bd1fbb5e",
       "peer_count":29,
       "high_fee_per_kb":0,
       "medium_fee_per_kb":0,
       "low_fee_per_kb":0,
       "unconfirmed_count":87914,
       "last_fork_height":6341457,
       "last_fork_hash":"f0484d9ffcd164fb1a57be2c56bef205f88d0259c4f178a65b01fae2745d7103"
       }, "luckynumber":20}
       **/

      WsBasis.takeCommitOnly(commit, "roulette_result", json)
    })

    socket_ws.On("initsub", function (json) {
      WsBasis.takeAllChannels(commit, "update_init_kj", "initsub", json)
    })
    socket_ws.On("gp", function (json) {
      // console.log ("stream upload ini pg", json);
      WsBasis.takeAllChannels(commit, "in_pg_update", "ingamepg", json)
    })
    socket_ws.On("kj", function (json) {
      WsBasis.takeAllChannels(commit, "in_kj", "ingamekj", json)
    })
    socket_ws.On("bet_confirm", function (json) {
      WsBasis.takeAllChannels(commit, "bet_confirm", "bet_confirm", json)
    })
    socket_ws.OnDisconnect(function () {
      EventBus.$emit("disconnect", true)
      //  document.getElementById("online_views").innerHTML = "you"ve been disconnected";
    })
    WsBasis.EventEmit(socket_ws, "submit_lotto_ticket_exec", "buy_ticket")
    WsBasis.EventEmit(socket_ws, "submit_lotto_ticket_save", "save_ticket")
    WsBasis.EventEmit(socket_ws, "check_result_transaction_id", "check_result_transaction_id")
  }
}
