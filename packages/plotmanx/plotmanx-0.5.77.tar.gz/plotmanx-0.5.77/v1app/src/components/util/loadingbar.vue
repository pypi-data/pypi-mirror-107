<template>

  <svg class="mainSVG" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <clipPath id="gradMask">
        <rect id="grad" x="100" y="280" width="400" height="36" rx="18" ry="18"/>
      </clipPath>
      <pattern id="gradPattern" width="400" height="36" x="0" y="0" patternUnits="userSpaceOnUse">
        <rect id="grad" x="0" y="0" fill="url(#xmasGrad)" width="400" height="36"/>
      </pattern>

      <filter id="drop" x="-150%" y="-150%" width="280%" height="280%">
        <feOffset result="offOut" in="SourceGraphic" dx="0" dy="0"/>
        <feGaussianBlur in="offOut" stdDeviation="19" result="blur"/>

        <feComponentTransfer>
          <feFuncA type="linear" slope="0.5"/>
        </feComponentTransfer>

        <feComposite in="SourceGraphic" operator="over"/>

      </filter>
    </defs>
    <linearGradient id="xmasGrad" gradientUnits="userSpaceOnUse" x1="0" y1="100" x2="400" y2="100">
      <stop offset="0" style="stop-color:#F2F6F6"/>
      <stop offset="0.1" style="stop-color:#F2F6F6"/>
      <stop offset="0.1" style="stop-color:#AF0404"/>
      <stop offset="0.2" style="stop-color:#AF0404"/>
      <stop offset="0.2" style="stop-color:#F2F6F6"/>
      <stop offset="0.3" style="stop-color:#F2F6F6"/>
      <stop offset="0.3" style="stop-color:#AF0404"/>
      <stop offset="0.4" style="stop-color:#AF0404"/>
      <stop offset="0.4" style="stop-color:#F2F6F6"/>
      <stop offset="0.5" style="stop-color:#F2F6F6"/>
      <stop offset="0.5" style="stop-color:#AF0404"/>
      <stop offset="0.6" style="stop-color:#AF0404"/>
      <stop offset="0.6" style="stop-color:#F2F6F6"/>
      <stop offset="0.7" style="stop-color:#F2F6F6"/>
      <stop offset="0.7" style="stop-color:#AF0404"/>
      <stop offset="0.8" style="stop-color:#AF0404"/>
      <stop offset="0.8" style="stop-color:#F2F6F6"/>
      <stop offset="0.9" style="stop-color:#F2F6F6"/>
      <stop offset="0.9" style="stop-color:#AF0404"/>
      <stop offset="1" style="stop-color:#AF0404"/>
    </linearGradient>

    <g filter="url(#drop)">
      <g clip-path="url(#gradMask)">
        <rect id="grad" x="100" y="268.8" fill="url(#gradPattern)" width="400" height="602.4"
              transform="matrix(1 0 0 1 100 -70) rotate(45 300 300)"/>
      </g>
    </g>
    <line id="shine" opacity="0.4" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"
          stroke-miterlimit="10" stroke-dasharray="346,6" x1="120" y1="289" x2="479" y2="289"/>
    <line id="shine" opacity="0.2" fill="none" stroke="#000" stroke-width="4" stroke-linecap="round"
          stroke-miterlimit="10" stroke-dasharray="0" x1="115" y1="314" x2="485" y2="314"/>

  </svg>

</template>

<script>
import { TweenMax, TimelineMax, Linear } from "gsap"

TweenMax.set("svg", {
  visibility: "visible"
})
const tl = new TimelineMax({ repeat: -1 })
tl.to("#gradPattern", 5, {
  attr: {
    x: 400
  },
  ease: Linear
})
export default {
  name: "Loadingbar"
}
</script>

<style scoped>

</style>
