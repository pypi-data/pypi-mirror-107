<template>
  <section>
    <canvas ref="canvas_instance_1"></canvas>
  </section>
</template>
<script>
/* global PIXI */
// import Waves from "../../plugins/pixi/shaders/waves"
import * as PIXI from "pixi.js"
import { TimelineLite, Back, Power2, Power1, GSDevTools } from "gsap"
import LoaderScreen from "../../plugins/pixi/LoaderScreen"
import { Assets } from "../../static/mmines/coksmse"
import basesnd from "../../plugins/mixins/minesweep/audiobase"
import sndmine from "../../plugins/mixins/minesweep/miniGameMines"

const GRADIENT = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAARElEQVQoU2PUDGj+z0AEYIyvmE2cwp65m4hTuH7vSeIUXrp7nziFd549I07hk9dviFP45uNH4hR+/vaNOIW///whSiEAEDQhEAWQi7IAAAAASUVORK5CYII="
/*  const IMG_DICE = "mmines/imgs/dice.png";
    const IMG_KRAKEN_ALIVE = "mmines/imgs/kraken_alive.png";
    const IMG_KRAKEN_DEAD = "mmines/imgs/kraken_dead.png";
  ; */
// const filter_map_ocean = "mmines/imgs/w32c.png";
// const filter_map_displacement = "mmines/imgs/displacement_map.png";
const DICE_SIZE = 50
const CANVAS_W = 400
const CANVAS_H = 400

function getGradientImage () {
  const image = new Image()
  image.src = GRADIENT

  const myBaseTexture = new PIXI.BaseTexture(image)
  const texture = new PIXI.Texture(myBaseTexture)

  // then add to the cache (if required)
  //   PIXI.Texture.addToCache (texture, "gra91213");

  // to retrieve the texture it would be a case of
  //  return PIXI.Sprite.from ("gra91213");
  return texture
}

function startRender (canvas, vue, callbacknext) {
  const loader = new LoaderScreen(vue.$store) // Basic Loading screen

  // console.log ("find out there");
  // console.log (canvas);
  // console.log (PIXI);
  // return

  const renderer = PIXI.autoDetectRenderer({
    backgroundColor: 0xFFFFFF,
    width: CANVAS_W,
    height: CANVAS_H,
    view: canvas,
    antialias: true,
    clearBeforeRender: true
  })

  // setup renderer and ticker
  // let renderer = new PIXI.Renderer ({ width : 800, height : 600, backgroundColor : 0x1099bb });
  // document.body.appendChild (renderer.view);
  // context = renderer.context;
  const stage = new PIXI.Container()

  loader.onLoaded(function (_load, resources) {
    //     context_src.packedim.spritesheet.textures[""]
    //     setup areas
    //  console.log (resources);
    callbacknext(renderer, stage, resources)

    requestAnimationFrame(animate)
  })
  // setup RAF
  let oldTime = Date.now()

  function animate () {
    const newTime = Date.now()
    let deltaTime = newTime - oldTime
    oldTime = newTime
    if (deltaTime < 0) { deltaTime = 0 }
    if (deltaTime > 1000) { deltaTime = 1000 }
    const deltaFrame = deltaTime * 60 / 1000 // 1.0 is for single frame
    // update your game there
    vue.$emit("engineUpdate", { dt: deltaTime, df: deltaFrame })
    renderer.render(stage)
    requestAnimationFrame(animate)
  }

  stage.addChild(loader)
  loader.start(Assets)
}

function getName (horizontal, vertical) {
  return "c" + horizontal + "-" + vertical
}

function generateMap (horizontal_count, vertical_count, generate) {
  let cell_id = 0
  // starts from zero
  for (let i = 0; i < vertical_count; i++) {
    for (let j = 0; j < horizontal_count; j++) {
      const ID_field = getName(j, i)
      // const chance = that.target_mines / that.total_balls;
      // const hit = Math.random () > chance;
      generate(cell_id, ID_field, j, i)
      cell_id++
    }
  }
}

function shuffle (array) {
  let currentIndex = array.length; let temporaryValue; let randomIndex
  // While there remain elements to shuffle...
  while (currentIndex !== 0) {
    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex)
    currentIndex -= 1
    // And swap it with the current element.
    temporaryValue = array[currentIndex]
    array[currentIndex] = array[randomIndex]
    array[randomIndex] = temporaryValue
  }
  return array
}

function addFilterWaves (targetSprite, res) {
  // console.log (res.filter_map_displacement);
  // return;
  // const txt = that.loadedRes.filter_map_displacement;
  // const texture_dis = PIXI.Texture.from (res.filter_map_displacement.texture);
  const texture_dis = res.filter_map_displacement.texture
  // const texture_dis = PIXI.Texture.from (filter_map_displacement);
  texture_dis.baseTexture.wrapMode = PIXI.WRAP_MODES.REPEAT
  const displacementSprite = new PIXI.Sprite(texture_dis)
  const wave_filter = new PIXI.filters.DisplacementFilter(displacementSprite)
  // wave_filter.scale.set (1.1, 1.2);
  wave_filter.scale.x = 70
  wave_filter.scale.y = 50
  targetSprite.filters = [wave_filter]
}

/*
    function gradient (fromo, to) {
      const c = document.createElement ("canvas");
      const ctx = c.getContext ("2d");
      const grd = ctx.createLinearGradient (0, 0, CANVAS_W, CANVAS_H);
      grd.addColorStop (0, fromo);
      grd.addColorStop (1, to);
      ctx.fillStyle = grd;
      ctx.fillRect (0, 0, 100, 100);
      return new PIXI.Texture.from (c);
    } */

class Chess {
  constructor () {
  }
}

// that.$GSLite = new TimelineLite ();
export default {
  name: "FieldMineV1",
  mixins: [basesnd, sndmine],
  data () {
    return {
      stage: null,
      renderer: null,
      areas: new Map(),
      total_balls: 0,
      target_mines: 1,
      loadedRes: null,
      requested_draw_loc: -1,
      confirmed_draw: false,
      playlock: false,
      pickhistory: [],
      showInAnimation: true
    }
  },
  mounted () {
    const that = this
    const { canvas_instance_1 } = that.$refs
    that.$nextTick(() => {
      startRender(canvas_instance_1, that,
        function (renderer, stage, src) {
          that.loadedRes = src
          that.stage = stage
          that.renderer = renderer
          //  console.log ("renderer");
          that.genOcean(stage)
          that.genWaves(stage)
          const all_dices = new PIXI.Container()
          stage.addChild(all_dices)
          that.keeper = all_dices

          // that.TestDebug ();
          // addFilterWaves (all_dices);
          that.startBgm()
        })
    })
  },
  created () {
    this.$store.dispatch("pixiUtil/setRenderSize", { canvasWidth: CANVAS_W, canvasHeight: CANVAS_H })

    /* this.addarea ();
       this.addarea ();
       this.addarea (); */
  },
  methods: {
    addarea () {
      /* this.areas.push ({
           x : 640 * (0.5 - Math.random ()),
           y : 480 * (0.5 - Math.random ()),
           angle : 2 * Math.PI * Math.random (),
           scale : 0.25 + 0.5 * Math.random (),
         }) */
    },
    genWaves (stage) {
      const that = this
      /*
        const waves = new PIXI.Graphics ().beginTextureFill (gradient ('#FCFCFC', '#95cffb'));
        waves.position.set (100);
        waves.pivot.set (50);
        const tex = PIXI.RenderTexture.create ({ width : CANVAS_W, height : CANVAS_H });
        that.renderer.render (waves, tex);
        const sprite_final = new PIXI.Sprite (tex);
        const simpleShader = new PIXI.Filter ('', Waves.SHADER_WAVE_C);
        waves.filters = [simpleShader]; */

      const tilingSprite = new PIXI.TilingSprite(getGradientImage(), CANVAS_W, CANVAS_H)
      let count = 0; const movement = 0.51; const scale_init = 50.11
      that.$on("engineUpdate", ({ dt, df }) => {
        count += 0.0005
        tilingSprite.tileScale.x = Math.sin(count) * 10 + scale_init
        tilingSprite.tileScale.y = Math.cos(count) * 5 + scale_init
        //  tilingSprite.tilePosition.x += movement;
        tilingSprite.tilePosition.y += movement
        // tilingSprite.rotation += movement;
      })
      addFilterWaves(tilingSprite, that.loadedRes)
      stage.addChild(tilingSprite)
      // tilingSprite.blendMode = PIXI.BLEND_MODES.B;
      tilingSprite.alpha = 0.5
    },

    genOcean (stage) {
      const that = this
      const txt = that.loadedRes.filter_map_ocean.texture
      //   console.log (txt);

      // const texture = PIXI.Texture.from (txt);

      const tilingSprite = new PIXI.TilingSprite(txt, CANVAS_W, CANVAS_H)
      let count = 0; const movement = 0.21; const scale_init = 0.11
      that.$on("engineUpdate", ({ dt, df }) => {
        count += 0.0005
        tilingSprite.tileScale.x = (Math.cos(count) + 1.5) / 4.1 + scale_init
        tilingSprite.tileScale.y = (Math.cos(count) + 1.5) / 8.5 + scale_init
        tilingSprite.tilePosition.x += Math.sin(count) * Math.sin(movement)
        tilingSprite.tilePosition.y += movement
      })
      //  tilingSprite.filters = [new PIXI.filters.ColorMatrixFilter ()];
      // tilingSprite.alpha = 1;
      // addFilterWaves (tilingSprite);
      stage.addChild(tilingSprite)
    },
    randomIslands (list) {
      const r = Math.floor(Math.random() * list.length)
      return list[r]
    },
    genDice (cid, meta, x, y /*, mine_hit */) {
      const that = this
      const txt = that.loadedRes.packedim.spritesheet.textures
      // console.log (that.loadedRes.packedim);
      // const ghost = PIXI.Texture.from (txt["kraken_alive.png"]);
      const ghost = txt.kraken_alive
      // const ghost2 = PIXI.Texture.from (txt["kraken_dead.png"]);
      const ghost2 = txt.kraken_dead
      const island1 = txt.island1_1
      const island2 = txt.island2_1
      const island3 = txt.island3_1
      const dice_simple = txt.dice
      const display_island = that.randomIslands([island1, island2, island3])
      // const area = PIXI.Sprite.from (txt["dice.png"]);
      const area = PIXI.Sprite.from(dice_simple)
      //  let area = PIXI.area.from ("~assets/img/dice.png");
      const magic_num = Math.random() * 25
      const MOVE_INDIVDUAL = 5
      //  console.log (area.width);
      //  console.log (area);
      const scale_expect = DICE_SIZE / area.width
      const sp1 = area.width / 2
      const sp2 = area.height / 2
      const basex = x + sp1 + Math.random() * MOVE_INDIVDUAL - MOVE_INDIVDUAL / 2
      const basey = y + sp2 + Math.random() * MOVE_INDIVDUAL - MOVE_INDIVDUAL / 2
      area.scale.x = scale_expect
      area.scale.y = scale_expect
      area.anchor.set(0.5)
      area.position.set(basex, basey)
      area.interactive = true
      area.buttonMode = true
      area.on("pointerdown", function () {
        if (!that.playlock) {
          that.$emit("request_pick_draw", {
            hash: "mckklmckkmklkodpowd",
            loc: cid,
            time: new Date()
          })
          that.requested_draw_loc = cid
          that.confirmed_draw = false
        }
      })
      let state = 0; let count = magic_num / 2; const savedx = area.position.x; const scx = 0.4

      that.$on("engineUpdate", ({ dt, df }) => {
        if (state === 0) {
          //  area.rotation += 0.01 * df;
          area.position.y = basey + Math.cos(0.01 * df) * 5
        } else if (state === 1) {
          count += 0.07
          area.scale.x = scx + (Math.sin(count * 1.232) + 1) * 0.01
          area.position.x = savedx + Math.sin(count)
        }
      })
      const Lite = new TimelineLite()

      function now_monster () {
        const monster = Math.random() > 0.1 ? ghost : ghost2
        area.texture = monster
        area.rotation = 0
        area.scale.set(scx, scx)
        const rotation = Math.floor(Math.random() * 360)
        const cmf = new PIXI.filters.ColorMatrixFilter()
        cmf.hue(rotation, true)
        area.filters = [cmf]
        state = 1
        that.sfxMonsterShow()
      }

      function destroy_resolved () {
        const fblur = new PIXI.filters.BlurFilter()
        const falpha = new PIXI.filters.AlphaFilter(0)
        // console.log (falpha);
        area.filters = [fblur, falpha]
        area.texture = display_island
        Lite
          .to(falpha, 2.2, { alpha: 1 })
          .to(fblur, 1.9, { blur: 0 })
          // Lite.to (onitem, 1, { alpha : 0, delay : 2 });
        state = 2
        that.sfxCityShow()
      }

      function disabled () {
        area.visible = false
        area.filters = []
      }

      function destroy_item () {
        const onitem = new PIXI.filters.BlurFilter()
        onitem.blur = 0
        area.filters = [onitem]
        Lite
          .to(area.position, 1, { y: basey + 10 })
          .to(onitem, 2, { blur: 100 })
          .eventCallback("onComplete", disabled)

        // Lite.to (onitem, 1, { alpha : 0, delay : 2 });
        // GSDevTools.create ();
        that.sfxResolve()
        state = 2
      }

      /*   const sortGroup = new PIXI.display.Group (1, ((plane) => {
             plane.zOrder = -plane.getDepth ();
           }));
           */

      /* offline use only
                that.$on ("touch_offline_play", (metaname) => {
                  if (metaname === meta) {
                    console.log (metaname);
                    if (mine_hit) {
                      now_monster ();
                    } else {
                      destroy_item ();
                    }
                    area.interactive = false;
                  }
                }); */

      that.$on("internal_show_monster", (loc_id) => {
        if (cid === loc_id && state !== 1) {
          now_monster()
        }
      })
      that.$on("internal_show_empty", (loc_id) => {
        if (cid === loc_id && state !== 2) {
          destroy_item()
        }
      })
      that.$on("internal_show_continue", (loc_id) => {
        if (cid === loc_id && state !== 2) {
          destroy_resolved()
        }
      })

      return { meta, area }
    },
    // only offline play
    clearAll () {
      const that = this
      that.areas = new Map()
      that.total_balls = 0
      that.pickhistory = []
      that.keeper.removeChildren(0)
    },
    showMonsters (list) {
      if (this.showInAnimation) {
        // with animations
        let sh = 0; let setloop = 0; const that = this; let ismonster = false
        const start_wait = 3000; const iterate_wait = 600
        that.playlock = true

        const iter = []

        for (let k = 0; k < 25; k++) {
          if (k !== that.requested_draw_loc && !this.pickhistory.includes(k)) {
            iter.push(k)
          }
        }

        that.$emit("internal_show_monster", that.requested_draw_loc)
        setTimeout(function () {
          setloop = setInterval(function () {
            if (sh < iter.length) {
              const check_i = iter[sh]
              ismonster = list.includes(check_i)
              if (ismonster) {
                that.$emit("internal_show_monster", check_i)
              } else {
                that.$emit("internal_show_empty", check_i)
              }
              sh++
            } else {
              console.log("animation invalid list: ", list)
              this.saftyComplete()
              clearInterval(setloop)
            }
          }, iterate_wait)
        }, start_wait)
      } else {
        // without animations
        if (typeof list === "object") {
          for (let n = 0; n < list.length; n++) {
            this.$emit("internal_show_monster", list[n])
          }
        } else {
          this.saftyComplete()
          console.log("no animation invalid list: ", list)
        }
      }
    },
    saftyComplete () {
      this.playlock = false
      this.$emit("draws_reveal_complete")
    },
    confirmSafe () {
      this.$emit("internal_show_continue", this.requested_draw_loc)
      // this.requested_draw_loc = cid;
      this.confirmed_draw = true
      if (!this.pickhistory.includes(this.requested_draw_loc)) {
        this.pickhistory.push(this.requested_draw_loc)
      }
    },
    OfflineStart (level, h, v) {
      const that = this
      that.target_mines = level
      that.clearAll()
      const fx = DICE_SIZE + 10
      const fy = DICE_SIZE + 10
      const offset = (CANVAS_W - h * (DICE_SIZE + 10)) / 2
      /**
         * testing only */
      const orders = []

      function gt () {
        return Math.floor(Math.random() * 25)
      }

      for (let n = 0; n < level; n++) {
        let m = gt()
        while (orders.includes(m)) {
          m = gt()
        }
        orders.push(m)
      }
      console.log(orders)
      generateMap(h, v, (cid, name, x, y) => {
        const isMonster = orders.includes(cid)
        const { meta, area } = that.genDice(cid, name, fx * x + offset, fy * y + offset, isMonster)
        that.keeper.addChild(area)
        that.areas.set(meta, area)
        that.total_balls++
      })
    },
    OnlineStart (h, v) {
      const that = this
      that.clearAll()
      const padding = 25
      const fx = DICE_SIZE + padding
      const fy = DICE_SIZE + padding
      const offset = (CANVAS_W - h * (DICE_SIZE + padding)) / 2
      generateMap(h, v, (cid, name, x, y) => {
        const { meta, area } = that.genDice(cid, name, fx * x + offset, fy * y + offset)
        that.keeper.addChild(area)
        that.areas.set(meta, area)
        that.total_balls++
      })
    },
    TestDebug () {
      const that = this
      that.OnlineStart(5, 5)
      const f = setInterval(function () {
        const c = Math.floor(Math.random() * 25)
        // that.$emit ("internal_show_monster", c);
        // that.$emit ("internal_show_empty", c);
        that.$emit("internal_show_continue", c)
      }, 1000)
    }
  }
}
</script>

<style scoped>

</style>
