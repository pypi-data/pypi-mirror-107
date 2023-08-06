import NewAudioSFX from "@/api/audio/audiomx"

const state = {
  Renderer: {
    canvasHeight: 0,
    canvasWidth: 0,
    height: 0,
    width: 0
  }
}

const mutations = {
  RENDER_SIZE (state, o) {
    state.Renderer.canvasHeight = o.canvasHeight
    state.Renderer.canvasWidth = o.canvasWidth
  }
}

const actions = {
  nextLoop ({ commit }) {
    commit("NEXT_LOOP")
  },
  toggleSFX ({ commit }) {
    commit("TOGGLE_SOUND")
  },
  toggleBGM ({ commit }) {
    commit("TOGGLE_SOUND_BGM")
  },
  addTrack ({ commit }, a) {
    commit("ADD_TRACK", a)
  },
  setRenderSize ({ commit }, size) {
    commit("RENDER_SIZE", size)
  },
  stopCurrentMusic ({ commit }) {
    commit("STOP_CURRENT")
  }
}
const getters = {
  isSNDEnabled (state) {
    return state.sfx_enabled
  },
  isBGMEnabled (state) {
    return state.bgm_enabled
  },
  audiotracks (state) {
    return state.audio_tracks
  },
  current_music (state) {
    return state.current_music
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
