<template>
  <simp-re v-if="isGameNotStarted"
           window_mask="std_window_mask"
           class="windowed_table_x"
           window_background_class="kz_window">
    <span slot="header" class="smaller">

    </span>
    <div slot="body">
      <div class="ugrid popbox">
        <div class="row">
          <div class="col col-12-of-12 r15basic center">
            <span class="h3">{{ $t("msg_new_round") }}}</span>
            <p>Counting Down in {{ gameStartIn }} seconds</p>
          </div>
        </div>
        <div class="row">
          <div class="col col-6-of-12 r18basic center" @click="clickredraw">
            F
          </div>
          <div class="col col-6-of-12 r18basic center" @click="clickredraw">
            V
          </div>
        </div>
      </div>
    </div>
    <div slot="footer">
      <span class="h3">{{ $t("msg_stay_tuned") }}</span>
    </div>
  </simp-re>
</template>

<script>
import W from "Web3"
import SimpRe from "../util/SimpRe"

export default {
  name: "RestartCntDn",
  components: { SimpRe },
  data () {
    return { withdrawlbox: false }
  },
  computed: {
    isGameNotStarted () {
      return !this.$store.getters["common/isCurrentRoundStarted"]
    },
    gameStartIn () {
      return this.$store.getters["common/sameStartInCountDown"]
    }
  },
  methods: {
    clickredraw (e) {
      e.preventDefault()
    },
    toEther (f) {
      return W.utils.fromWei(f + "", "ether")
    }
  }
}
</script>
