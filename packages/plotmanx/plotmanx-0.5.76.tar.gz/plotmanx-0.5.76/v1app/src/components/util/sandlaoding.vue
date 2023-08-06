<template>
  <div class="c-loader">
    <svg version="1.1" class="c-loader__svg" xmlns="http://www.w3.org/2000/svg" x="0" y="0" viewBox="0 0 104 176"
         xml:space="preserve">
      <path class="c-loader__scaffolding"
            d="M0 12v12h8v40h8v8h8v8h8v16h-8v8h-8v8H8v40H0v24h104v-24h-8v-40h-8v-8h-8v-8h-8V80h8v-8h8v-8h8V24h8V0H0v12zm88 0v4H16V8h72v4zm0 28v16h-8v8h-8v8h-8v8h-8v16h8v8h8v8h8v8h8v32H16v-32h8v-8h8v-8h8v-8h8V80h-8v-8h-8v-8h-8v-8h-8V24h72v16zm0 124v4H16v-8h72v4z"/>
      <path d="M24 36v4h8v-8h-8v4z" class="c-loader__block1"/>
      <path d="M40 36v4h8v-8h-8v4z" class="c-loader__block2"/>
      <path d="M56 36v4h8v-8h-8v4z" class="c-loader__block3"/>
      <path d="M72 36v4h8v-8h-8v4z" class="c-loader__block4"/>
      <path d="M32 44v4h8v-8h-8v4z" class="c-loader__block5"/>
      <path d="M48 44v4h8v-8h-8v4z" class="c-loader__block6"/>
      <path d="M64 44v4h8v-8h-8v4z" class="c-loader__block7"/>
      <path d="M40 52v4h8v-8h-8v4z" class="c-loader__block8"/>
      <path d="M56 52v4h8v-8h-8v4z" class="c-loader__block9"/>
      <path d="M48 60v4h8v-8h-8v4z" class="c-loader__block10"/>
      <path d="M48 76v4h8v-8h-8v4z" class="c-loader__block11"/>
      <path d="M48 108v4h8v-8h-8v4z" class="c-loader__block12"/>
    </svg>
  </div>
</template>

<script>
import { TimelineMax } from "gsap"

export default {
  name: "Sandlaoding",
  mounted() {
    this.$nextTick(() => {
      /**
       * Old school Window Loader with GSAP
       * @author Daphne Smit <hi@daphnesmit.nl>
       */
      const delay = 0.08
      const tl = new TimelineMax({
        repeat: -1,
        repeatDelay: delay
      })

      tl
        .to(".c-loader__block1", 0, {
          opacity: 0,
          delay
        }, delay)
        .to(".c-loader__block11", 0, {
          x: 0,
          y: 24,
          delay
        }, delay)
        .to(".c-loader__block12", 0, {
          x: -8,
          y: 40,
          delay
        }, delay)

        .to(".c-loader__block1", 0, {
          opacity: 1,
          x: 24,
          y: 72,
          delay: delay * 2
        }, delay * 2)
        .to(".c-loader__block3", 0, {
          x: -8,
          y: 40,
          delay: delay * 2
        }, delay * 2)
        .to(".c-loader__block11", 0, {
          x: 8,
          y: 72,
          delay: delay * 2
        }, delay * 2)

        .to(".c-loader__block1", 0, {
          x: 24,
          y: 104,
          delay: delay * 3
        }, delay * 3)
        .to(".c-loader__block3", 0, {
          x: -8,
          y: 64,
          delay: delay * 3
        }, delay * 3)
        .to(".c-loader__block4", 0, {
          x: -24,
          y: 64,
          delay: delay * 3
        }, delay * 3)

        .to(".c-loader__block2", 0, {
          x: 8,
          y: 72,
          delay: delay * 4
        }, delay * 4)
        .to(".c-loader__block3", 0, {
          x: 16,
          y: 112,
          delay: delay * 4
        }, delay * 4)
        .to(".c-loader__block4", 0, {
          x: -24,
          y: 40,
          delay: delay * 4
        }, delay * 4)

        .to(".c-loader__block2", 0, {
          x: -8,
          y: 104,
          delay: delay * 5
        }, delay * 5)
        .to(".c-loader__block4", 0, {
          x: -24,
          y: 64,
          delay: delay * 5
        }, delay * 5)
        .to(".c-loader__block6", 0, {
          x: 0,
          y: 56,
          delay: delay * 5
        }, delay * 5)

        .to(".c-loader__block4", 0, {
          x: -48,
          y: 112,
          delay: delay * 6
        }, delay * 6)
        .to(".c-loader__block5", 0, {
          x: 16,
          y: 64,
          delay: delay * 6
        }, delay * 6)
        .to(".c-loader__block6", 0, {
          x: 0,
          y: 32,
          delay: delay * 6
        }, delay * 6)

        .to(".c-loader__block5", 0, {
          x: 32,
          y: 96,
          delay: delay * 7
        }, delay * 7)
        .to(".c-loader__block6", 0, {
          x: 0,
          y: 56,
          delay: delay * 7
        }, delay * 7)
        .to(".c-loader__block7", 0, {
          x: -16,
          y: 56,
          delay: delay * 7
        }, delay * 7)

        .to(".c-loader__block6", 0, {
          x: 8,
          y: 88,
          delay: delay * 8
        }, delay * 8)
        .to(".c-loader__block7", 0, {
          x: -16,
          y: 64,
          delay: delay * 8
        }, delay * 8)
        .to(".c-loader__block9", 0, {
          x: -8,
          y: 24,
          delay: delay * 8
        }, delay * 8)

        .to(".c-loader__block7", 0, {
          x: -24,
          y: 88,
          delay: delay * 9
        }, delay * 9)
        .to(".c-loader__block8", 0, {
          x: 8,
          y: 24,
          delay: delay * 9
        }, delay * 9)
        .to(".c-loader__block9", 0, {
          x: -8,
          y: 56,
          delay: delay * 9
        }, delay * 9)

        .to(".c-loader__block8", 0, {
          x: 8,
          y: 48,
          delay: delay * 10
        }, delay * 10)
        .to(".c-loader__block9", 0, {
          x: -8,
          y: 72,
          delay: delay * 10
        }, delay * 10)
        .to(".c-loader__block10", 0, {
          x: 0,
          y: 40,
          delay: delay * 10
        }, delay * 10)

        .to(".c-loader__block8", 0, {
          x: 8,
          y: 72,
          delay: delay * 11
        }, delay * 11)
        .to(".c-loader__block10", 0, {
          x: 0,
          y: 64,
          delay: delay * 11
        }, delay * 11)

        .to(".c-loader__svg", 0, {
          rotation: -45,
          delay: delay * 12
        }, delay * 12)
        .to(".c-loader__block1", 0, {
          rotation: -45,
          x: 20,
          y: 110,
          delay: delay * 12
        }, delay * 12)
        .to(".c-loader__block2", 0, {
          rotation: -45,
          x: -7,
          y: 110,
          delay: delay * 12
        }, delay * 12)
        .to(".c-loader__block3", 0, {
          rotation: -45,
          x: -23,
          y: 88,
          delay: delay * 12
        }, delay * 12)
        .to(".c-loader__block4", 0, {
          rotation: -45,
          x: -50,
          y: 110,
          delay: delay * 12
        }, delay * 12)
        .to(".c-loader__block5", 0, {
          rotation: -45,
          x: 23,
          y: 102,
          delay: delay * 12
        }, delay * 12)
        .to(".c-loader__block6", 0, {
          rotation: -45,
          x: 18,
          y: 102,
          delay: delay * 12
        }, delay * 12)
        .to(".c-loader__block7", 0, {
          rotation: -45,
          x: -20,
          y: 91,
          delay: delay * 12
        }, delay * 12)
        .to(".c-loader__block8", 0, {
          rotation: -45,
          x: 4,
          y: 72,
          delay: delay * 12
        }, delay * 12)
        .to(".c-loader__block9", 0, {
          rotation: -45,
          x: -12,
          y: 61,
          delay: delay * 12
        }, delay * 12)
        .to(".c-loader__block10", 0, {
          rotation: -45,
          x: 7,
          y: 75,
          delay: delay * 12
        }, delay * 12)
        .to(".c-loader__block11", 0, {
          rotation: -45,
          x: -15,
          y: 59,
          delay: delay * 12
        }, delay * 12)
        .to(".c-loader__block12", 0, {
          rotation: -45,
          x: -26,
          y: 27,
          delay: delay * 12
        }, delay * 12)

        .to(".c-loader__svg", 0, {
          rotation: -90,
          delay: delay * 13
        }, delay * 13)
        .to(".c-loader__block6", 0, {
          rotation: -45,
          x: 7,
          y: 80,
          delay: delay * 13
        }, delay * 13)

        .to(".c-loader__svg", 0, {
          rotation: -135,
          delay: delay * 14
        }, delay * 14)
        .to(".c-loader__block5", 0, {
          rotation: -45,
          x: 23,
          y: 69,
          delay: delay * 14
        }, delay * 14)
    })
  }
}
</script>

<style scoped>

.c-loader {
  width: 104px;
}

</style>
