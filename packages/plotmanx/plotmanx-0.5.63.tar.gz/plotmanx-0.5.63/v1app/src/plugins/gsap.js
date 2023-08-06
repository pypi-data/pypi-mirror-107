import Vue from "vue"
import { TimelineLite, TimelineMax, TweenLite, TweenMax } from "gsap/all"
import Draggable from "gsap/Draggable"
import MotionPathPlugin from "gsap/MotionPathPlugin"
import MorphSVGPlugin from "gsap/MorphSVGPlugin"
import ScrollToPlugin from "gsap/ScrollToPlugin"
import ScrollTrigger from "gsap/ScrollTrigger"
import CSSPlugin from "gsap/CSSPlugin"
import DrawSVGPlugin from "gsap/DrawSVGPlugin"
import ScrambleTextPlugin from "gsap/ScrambleTextPlugin"
import Physics2DPlugin from "gsap/Physics2DPlugin"
// import DrawSVGPlugin from "@/plugins/gsapsvg";
import gsap from "gsap"
// don't forget to register plugins
gsap.registerPlugin(
  TimelineLite, TimelineMax, TweenMax,
  DrawSVGPlugin, ScrollTrigger, Draggable, MotionPathPlugin,
  ScrollToPlugin, Physics2DPlugin, MorphSVGPlugin, ScrambleTextPlugin, CSSPlugin)
// TweenMax, TweenLite, TimelineMax, TimelineLite,
const module = {
  install: (Vue, opts) => {
    //    that.$GSLite = new TimelineLite ();
    Vue.prototype.$gsapTimeLine = function (data) {
      return gsap.timeline(data)
    }
    Vue.prototype.GSAP = function (data) {
      return gsap
    }
  }
}

Vue.use(module)
