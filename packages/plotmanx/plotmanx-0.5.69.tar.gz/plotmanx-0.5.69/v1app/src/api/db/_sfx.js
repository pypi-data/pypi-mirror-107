import NewAudioSFX from "@/api/audio/audiomx"

const state = {
  current_music: null,
  current_play_sfx: null,
  music_clip_pos: 0,
  sfx_enabled: false,
  bgm_enabled: false,
  audio_tracks: []
}

const mutations = {
  TOGGLE_SOUND (state) {
    state.sfx_enabled = !state.sfx_enabled
  },
  TOGGLE_SOUND_BGM (state) {
    state.bgm_enabled = !state.bgm_enabled
  },
  ADD_TRACK (state, track) {
    state.audio_tracks.push(track)
    const lenaudio = state.audio_tracks.length
    if (lenaudio > 20) {
      state.audio_tracks.shift()
    }
  },
  SET_CURRENT_MUZIE (state, track) {
    state.current_music = track
  },
  SET_CURRENT_SFX (state, track) {
    state.current_play_sfx = track
  },
  NEXT_LOOP (state) {
    state.music_clip_pos++
    state.music_clip_pos = state.music_clip_pos % state.audio_tracks.length
  },
  STOP_CURRENT (state) {
    if (state.current_music instanceof NewAudioSFX) {
      state.current_music.SFXStop()
      state.bgm_enabled = false
    }
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
  setCurrentMuz ({ commit }, track) {
    commit("SET_CURRENT_MUZIE", track)
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
