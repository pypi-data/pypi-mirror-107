export default {
  data () {
    return {
      audio: {
        failure_click: this.SFX("sound/error.mp3"),
        bet_adjust: this.SFX("sound/chbet.mp3"),
        click_ui_sys: this.SFX("sound/ui2.mp3"),
        cash_out: this.SFX("sound/cashout.mp3")
      },
      loop: {
        game_play_music1: this.SFX("sound/resolved.mp3")
      },
      audio_music_loop: []
    }
  },
  mounted () {
    /*    for (let [k, v] in Object.entries (this.loop)) {
          this.audio_music_loop.push (k)
        } */
    this.$store.dispatch("sfx/setCurrentMuz", this.loop.game_play_music1)
  },
  methods: {
    GetLoopz () {
      return this.RandomizeTracks([
        this.loop.game_play_music1
      ])
    },
    GetMusicLoop (betted) {
      if (betted) {
        return this.GetLoopz()
      } else {
        return this.GetLoopz()
      }
    }
    // SFXSmartPlay
  }
}

// failure_click : this.SFX ("static/media/chart_corn.mp3"),
// start_bet : this.SFX ("static/media/button_confirm_bet.mp3"),
//  click_ui_sys : this.SFX ("static/media/change_bet.mp3"),
//  bet_adjust : this.SFX ("static/media/change_bet.mp3"),
// result_show : this.SFX ("static/media/outrun2_endC.mp3"),
// bet_music : this.SFX ("static/media/or_bet_music.mp3"),
// explode : this.SFX ("static/media/mgs_rank_AB.mp3"),
