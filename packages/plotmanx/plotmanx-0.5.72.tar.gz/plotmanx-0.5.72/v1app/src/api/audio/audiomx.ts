// tslint:disable:no-consecutive-blank-lines ordered-imports align trailing-comma enum-naming
// tslint:disable:whitespace no-unbound-method no-trailing-whitespace no-camelcase
// tslint:disable:no-unused-variable
import { TweenLite, Power1 } from "gsap"

export default class NewAudioSFX {
  _audio: any;
  _enabled: boolean;
  _gs: TweenLite;

  constructor(path) {
    // @ts-ignore
    this._gs = new TweenLite()
    this._audio = new Audio(path)
    this._audio.crossOrigin = "anonymous"
    this._audio.currentTime = 0
    this._audio.loop = false
    this._audio.autoplay = false
    this._enabled = false
  }

  muzPlay(enabled) {
    if (this._audio.canPlayType("audio/mpeg")) {
      const that = this
      this._audio.autoplay = false
      this._audio.currentTime = 0
      this._audio.loop = true
      if (!enabled) {
        this.setVolume(0)
      }
      that._audio.addEventListener("canplaythrough", function () {
        if (typeof that._audio.play === "function") {
          that._audio.play()
        }
        // console.log(that._audio)
      }, false)
      this._enabled = enabled
    } else {
      console.error("does not support mpeg format")
    }
  }

  setEnable(enabled: boolean) {
    if (this._audio === undefined) { return }
    const nowplay = this._audio.currentTime > 0
    if (enabled) {
      if (nowplay) {
        this.fadeInFast()
      } else {
        // this._audio.play();
      }
    } else if (nowplay) {
      this.fadeOutStop()
    }
    this._enabled = enabled
  }

  SFXStop() {
    // this._audio.currentTime = 0;
    if (typeof this._audio.setCurrentTime === "function") {
      this._audio.setCurrentTime(0)
    }
    this._audio.pause()
  }

  SFXNoSound() {
    if (!this._audio.paused) {
      this._audio.volume = 0
    }
  }

  SFXResumeSound(x: any) {
    if (!this._audio.paused) {
      if (typeof x === "boolean") {
        this._audio.volume = 1
      }
      if (typeof x === "number") {
        const g = Math.abs(x)
        if (g > 0 && g <= 100) {
          this._audio.volume = x / 100
        }
        if (g > 0 && g <= 1) {
          this._audio.volume = g
        }
      }
    }
  }

  SFXSmartPlayRandVolume() {
    this.setVolume(Math.random() * 0.9 + 0.1)
    this._audio.setCurrentTime(0)
    this._audio.play()
  }

  SFXPlay() {
    if (this._audio.canPlayType("audio/mpeg")) {
      this._audio.volume = 1
      this._audio.autoplay = false
      this._audio.currentTime = 0
      if (typeof this._audio.play === "function") {
        this._audio.play()
      }
    } else {
      console.error("does not support mpeg format")
    }
  }

  SFXStopEnd(audiox: any) {
    console.log(audiox)
    console.log("===")
    //  audiox.setCurrentTime(0);
    // audiox.pause();
  }

  setVolume(h: number) {
    this._audio.volume = h
  }

  fadeInFast() {
    // @ts-ignore
    this._gs.to(this._audio, 1, { volume: 1, ease: Power1.easeOut, delay: 0.0 })
  }

  fadeOut(callback?: object) {
    // @ts-ignore
    this._gs.to(this._audio, 2, { volume: 0, ease: Power1.easeOut, delay: 0.1 })
    // @ts-ignore
    this._gs.eventCallback("onComplete", callback, [this])
  }

  fadeOutStop() {
    console.log(this._audio)
    console.log("===ch")
    // @ts-ignore
    this._gs.to(this._audio, 2, { volume: 0, ease: Power1.easeOut, delay: 0.1 })
    this._gs.eventCallback("onComplete", this.SFXStopEnd, [this._audio])
  }

  fadeOutLast(sec: number, callback?: object) {
    // @ts-ignore
    this._gs.to(this._audio, sec, { volume: 0, ease: Power1.easeOut, delay: 0.1 })
    // @ts-ignore
    this._gs.eventCallback("onComplete", callback, [this])
  }

  static randSFXList(audios: Array<NewAudioSFX>) {
    const r = Math.floor(Math.random() * audios.length)
    return audios[r]
  }
}
