export default {
  data () {
    return {
      fxSnd: {
        question_double: new Audio("/media/questions_glass.mp3"),
        click: new Audio("https://freesound.org/data/previews/269/269504_3094998-lq.mp3"),
        error: new Audio("/media/credit_n2.mp3"),
        game_win_x1: new Audio("/media/credit_n1.mp3"),
        game_win_x2: new Audio("/media/credit_n2.mp3"),
        game_win_x3: new Audio("/media/win_ex_92.mp3")
      },

      loop: {
        main: new Audio("/media/monster_strike_main.mp3"),
        sp1: new Audio("/media/monster_strike_main.mp3"),
        sp3: new Audio("/media/monster_strike_main.mp3"),
        spafter: new Audio("/media/monster_strike_main.mp3"),
        spaftq: new Audio("/media/monster_strike_main.mp3")
      },
      current_music: null,
      music_clip_pos: 0,
      music_on: false
    }
  },
  methods: {
    playFxWinX1 () {
      this.trySndPlay("game_win_x1")
    },
    playFxWinX2 () {
      this.trySndPlay("game_win_x2")
    },
    playFxWinX3 () {
      this.trySndPlay("game_win_x3")
    },
    playNewTicket () {
      this.trySndPlay("question_double")
    },
    trySndPlay (x) {
      if (!this.fxSnd[x].isPlaying) {
        this.fxSnd[x].play()
      }
    },
    playMusic () {
      const index = this.nextLoop()
      this.getLoop()[index].play()
      this.music_on = true
      this.current_music = this.getLoop()[index]
    },
    stopaudio () {
      if (this.current_music instanceof Audio) {
        this.current_music.pause()
        this.current_music.currentTime = 0
        this.music_on = false
      }
    },
    nextLoop () {
      this.music_clip_pos++
      return this.music_clip_pos % this.getLoop().length
    },
    getLoop () {
      if (this.status_machine === 1 || this.status_machine === 0) {
        return [this.loop.main, this.loop.sp1, this.loop.sp3]
      } else {
        return [this.loop.spafter, this.loop.spaftq]
      }
    },
    toggleMusic () {
      if (!this.music_on) {
        this.playMusic()
      } else {
        this.stopaudio()
      }
    }
  }
}
