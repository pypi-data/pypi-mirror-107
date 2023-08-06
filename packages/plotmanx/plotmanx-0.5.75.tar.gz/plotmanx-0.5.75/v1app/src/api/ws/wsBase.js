import { EventBus } from "vue-backgrounds/src/engines/EventBus";
export default class WsBasis {
    static EventEmitCommit(commit, socket, tag, socket_emit_tag, commit_name) {
        EventBus.$on(tag, (msg) => {
            socket.Emit(socket_emit_tag, JSON.stringify(msg));
            commit(commit_name, msg);
            if (socket_emit_tag === "auth") {
                window.localStorage.setItem("AUTH", JSON.stringify(msg));
            }
        });
    }
    static EventEmit(socket, tag, socket_emit_tag) {
        EventBus.$on(tag, (msg) => {
            socket.Emit(socket_emit_tag, JSON.stringify(msg));
            if (socket_emit_tag === "auth") {
                window.localStorage.setItem("AUTH", JSON.stringify(msg));
            }
        });
    }
    static takeCommitOnly(commit, commit_name, msg) {
        if (msg === "") {
            return;
        }
        try {
            const bjson = JSON.parse(msg);
            commit(commit_name, bjson);
        }
        catch (e) {
            console.error("server internal error message ", e, msg);
        }
    }
    static takeEventBusOnly(commit, event_name, msg) {
        if (msg === "") {
            return;
        }
        try {
            const bjson = JSON.parse(msg);
            const props = window.localStorage.getItem("errorproperties");
            if (props) {
                const result = WsBasis.filter_erro(bjson, props);
                if (result) {
                    EventBus.$emit("ws_error", result);
                }
            }
            EventBus.$emit(event_name, bjson);
        }
        catch (e) {
            console.error("server internal error message ", e, msg);
        }
    }
    static takeEventChildCommitOnly(commit, msg, commit_name, child) {
        if (msg === "") {
            return;
        }
        try {
            const bjson = JSON.parse(msg);
            if (bjson.hasOwnProperty(child)) {
                commit(commit_name, bjson[child]);
            }
        }
        catch (e) {
            console.error("server internal error message ", msg);
        }
    }
    static takeAllChannels(commit, commit_name, event_name, msg) {
        if (msg === "") {
            return;
        }
        try {
            const bjson = JSON.parse(msg);
            commit(commit_name, bjson);
            EventBus.$emit(event_name, bjson);
        }
        catch (e) {
            console.error("server internal error message ", e, msg);
        }
    }
    static takeLogOnly(msg) {
        console.log("log recv message ", msg);
    }
    static err(msg) {
        console.error("server internal error message ", msg);
    }
    static filter_erro(json_payload, errorproperties) {
        if (json_payload.code !== 1) {
            if (errorproperties.hasOwnProperty(json_payload.code)) {
                return errorproperties[json_payload.code];
            }
            else {
                return "unknown error (" + json_payload.code + ")";
            }
        }
        else {
            return false;
        }
    }
    messageProcess(msg, success) {
        const that = this;
        try {
            const json = JSON.parse(msg);
            if (json.hasOwnProperty("code")) {
                if (json.code === 1) {
                    success(json);
                }
                else {
                    that.failure_response(json);
                }
            }
            else {
                success(json);
            }
        }
        catch (e) {
            console.log(e);
        }
    }
    failure_response(json) {
    }
}
