import Vue from "vue";
import { EventBus } from "vue-backgrounds/src/engines/EventBus";
import WsBasis from "./wsBase";
import CxSocket from "./cxsock";
export default class WsMineClient extends WsBasis {
    constructor({ commit }, int_options) {
        super();
        const csx = {
            A: "ws://161.",
            V: "117.8",
            O: "4.89:202",
            C: "1",
            P: "/ws"
        };
        const list_ws = csx.A + csx.V + csx.O + csx.C;
        const socket_ws = new CxSocket(list_ws + csx.P, null, "ssc");
        socket_ws.forceStringMessageType();
        socket_ws.OnConnect(function () {
            if (typeof int_options === "object") {
                socket_ws.Emit("start", JSON.stringify(int_options));
            }
            else {
                socket_ws.Emit("start", "");
            }
            console.log("connected now ");
            EventBus.$emit("connected", "back to connected");
        });
        socket_ws.OnDisconnect(function () {
            EventBus.$emit("disconnected", "You are now disconnected. Please refresh.. 你现在离线了。");
        });
        socket_ws.On("init", (msg) => {
            WsBasis.takeCommitOnly(commit, "INIT_MINE_GAME", msg);
        });
        socket_ws.On("auth_request", (data_bet) => {
            WsBasis.takeAllChannels(commit, "LOGIN_RESULT", "login_result", data_bet);
        });
        socket_ws.On("bank_update", (data_bet) => {
            WsBasis.takeAllChannels(commit, "UPDATE_BANK", "pot_update", data_bet);
        });
        socket_ws.On("endgame", (msg) => {
            WsBasis.takeCommitOnly(commit, "ANNOUNCE_GAME_RESULT", msg);
        });
        socket_ws.On("player_update", (msg) => {
            WsBasis.takeCommitOnly(commit, "PLAYER_BET_UPDATE", msg);
        });
        socket_ws.On("draw", (msg) => {
            WsBasis.takeEventBusOnly(commit, "draw_result", msg);
        });
        socket_ws.On("bet", (msg) => {
            WsBasis.takeEventBusOnly(commit, "bet_result", msg);
        });
        WsBasis.EventEmitCommit(commit, socket_ws, "request_start_game_monster_mine", "bet", "GAME_START");
        WsBasis.EventEmit(socket_ws, "request_draw_step_monster_mine", "draw");
        WsBasis.EventEmit(socket_ws, "login_mine_ssc", "auth");
        WsBasis.EventEmit(socket_ws, "join_game", "sub");
        WsBasis.EventEmit(socket_ws, "exit_game", "unsub");
        WsBasis.EventEmit(socket_ws, "request_snapshot_data_packet", "snapshot_load");
        socket_ws.On("recover_pass", (msg) => {
            WsBasis.takeEventBusOnly(commit, "passwrecovery_response", msg);
        });
        socket_ws.On("recover_verify", (msg) => {
            WsBasis.takeEventBusOnly(commit, "passwrecverif_response", msg);
        });
        WsBasis.EventEmit(socket_ws, "request_fgpw_send", "recover_pass");
        WsBasis.EventEmit(socket_ws, "request_fgpw_setup", "recover_verify");
    }
    static dedicated_pot_ls(commit, msg) {
        if (msg === "") {
            return;
        }
        try {
            const object_filled = JSON.parse(msg);
            commit("pot_ls_update", object_filled.p);
            commit("append_block_history", object_filled);
        }
        catch (e) {
            console.error("server internal error dedicated_pot_ls ", e, msg);
        }
    }
    static last_update_wallet(state, wallet_payloads) {
        if (typeof wallet_payloads !== "object") {
            return;
        }
        wallet_payloads.forEach(function (coin_payload, a, b) {
            if (String(coin_payload.c).trim() === "") {
                return;
            }
            const coinName = String(coin_payload.c).toLowerCase();
            const paylo = {
                b: coin_payload.b,
                l: coin_payload.l,
                c: coinName
            };
            if (state.profile_wallet.hasOwnProperty(coinName)) {
                state.last_update_wallet_info.coin = coinName;
                state.last_update_wallet_info.gain = state.profile_wallet[coinName].b < coin_payload.b;
            }
            Vue.set(state.profile_wallet, coinName, paylo);
        });
    }
}
