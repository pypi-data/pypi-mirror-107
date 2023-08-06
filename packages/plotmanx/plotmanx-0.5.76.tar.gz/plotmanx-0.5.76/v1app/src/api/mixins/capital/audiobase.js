import { TimelineLite, Back, Power2, Power1 } from "gsap"
import NewAudioSFX from "../../audio/audiomx"
// delay:0.1,
//  ease:Power2.easeInOut
export default {
  destroyed () {
    if (this.current_play_sfx instanceof NewAudioSFX) {
      this.current_play_sfx.SFXStop()
    }
    if (this.current_music instanceof NewAudioSFX) {
      this.current_music.SFXStop()
    }
  },
  computed: {
    current_music () {
      return this.$store.getters["sfx/current_music"]
    },
    audio_tracks () {
      return this.$store.getters["sfx/audiotracks"]
    },
    sfx_enabled () {
      return this.$store.getters["sfx/isSNDEnabled"]
    },
    bgm_enabled () {
      return this.$store.getters["sfx/isBGMEnabled"]
    }
  },
  methods: {
    SFX (path) {
      //  console.log ("load ", path);
      return new NewAudioSFX(path)
    },
    RandomizeTracks (list) {
      return NewAudioSFX.randSFXList(list)
    },
    startBgm () {
      if (this.current_music instanceof NewAudioSFX) {
        this.current_music.muzPlay(this.bgm_enabled)
      }
    },
    stopMuzAudio () {
      if (this.current_music instanceof NewAudioSFX) {
        this.current_music.SFXStop()
        this.bgm_enabled = false
      }
    },
    onSFXComplete (audio_instance) {
      if (audio_instance instanceof NewAudioSFX) {
        audio_instance.SFXStop()
      }
    },
    SFXSmartPlay (audio_instance) {
      if (audio_instance instanceof NewAudioSFX) {
        if (this.sfx_enabled) {
          audio_instance.SFXPlay()
        }
      }
    },
    SFXFadeOut (target, span_sec) {
      if (target === undefined) { return }
      if (target instanceof NewAudioSFX) {
        target.fadeOutLast(span_sec, this.onSFXComplete)
      }
    },
    SFxEndGame () {
    },
    SFXFailure () {
    },
    SfxGameStart () {
      if (this.sfx_enabled) {
      }
    },
    SFxClick () {
      if (this.sfx_enabled) {
        this.audio.click_ui_sys.SFXPlay()
      }
    },
    betadjust () {
      if (this.sfx_enabled) {
        this.audio.bet_adjust.SFXPlay()
      }
    },
    cashOut () {
      if (this.sfx_enabled) {
        this.audio.cash_out.SFXPlay()
      }
    },
    SFxUIClick () {
      this.audio.click_ui_sys.SFXPlay()
    },
    SFxStartBet () {
    },
    SFxESC () {
      if (this.sfx_enabled) {
        this.audio.start_esc.SFXPlay()
      }
    },
    trySndPlay (x) {
      if (this.audio[x].paused) {
        this.audio[x].SFXPlay()
      }
    },
    stopSetup (x) {
      if (this.audio[x] !== undefined) {
        if (!this.audio[x].paused) {
          this.audio[x].SFXStop()
        }
      }

      if (this.loop[x] !== undefined) {
        if (!this.loop[x].paused) {
          this.loop[x].SFXStop()
        }
      }
    },
    toggle_audio_switch () {
      this.$store.dispatch("sfx/toggleSFX")
      this.$store.dispatch("sfx/toggleBGM")
      if (!this.sfx_enabled) {
        if (this.current_music instanceof NewAudioSFX) {
          this.current_music.setEnable(false)
        }
      } else if (this.current_music instanceof NewAudioSFX) {
        this.current_music.setEnable(true)
      }

      //  console.log ("toggle music");
      // if (!this.sfx_enabled) {
      //  this.playMusic ();
      // } else {
      //  this.stopAudio ();
      // }

      if (this.sfx_enabled) {
        this.notificationInfo("SFX is ON")
      } else {
        this.notificationInfo("SFX is OFF")
      }
    }
  }
}
