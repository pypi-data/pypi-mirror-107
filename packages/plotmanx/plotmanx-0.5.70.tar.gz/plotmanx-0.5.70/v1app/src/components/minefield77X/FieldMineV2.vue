<template>
  <section>
    <pixi-renderer
      :background-color="0x0078FF"
      :height="600"
      :width="600"
      @tick="update">
      <pixi-container
        :x="320" :y="240"
        :rotation="-t / 40">
        <pixi-sprite v-for="(sprite, key) in sprites" :key="key"
                     :x="sprite.x"
                     :y="sprite.y" :scale-x="sprite.scale"
                     :scale-y="sprite.scale" :anchor-x="0.5"
                     :anchor-y="0.5" :rotation="sprite.angle + t / 60"
                     src="mmines/imgs/dice.png"/>
      </pixi-container>
    </pixi-renderer>
  </section>
</template>

<script>
import PixiRenderer from "vue-pixi-onode/src/components/Renderer"
import PixiContainer from "vue-pixi-onode/src/components/Container"
import PixiSprite from "vue-pixi-onode/src/components/Sprite"

export default {
  name: "FieldMineCore",
  components: { PixiRenderer, PixiContainer, PixiSprite },
  data () {
    return { t: 0, sprites: [] }
  },
  created () {
    this.addSprite()
    this.addSprite()
    this.addSprite()
  },
  methods: {
    addSprite () {
      this.sprites.push({
        x: 640 * (0.5 - Math.random()),
        y: 480 * (0.5 - Math.random()),
        angle: 2 * Math.PI * Math.random(),
        scale: 0.25 + 0.5 * Math.random()
      })
    },
    update (dt) {
      this.t += dt
    }
  }

}
</script>

<style scoped>

</style>
