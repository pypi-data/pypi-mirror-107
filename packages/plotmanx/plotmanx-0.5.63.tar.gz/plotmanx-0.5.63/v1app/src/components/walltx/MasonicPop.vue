<template>
  <simp-re v-if="withdrawlbox"
           window_mask="std_window_mask"
           class="windowed_table_x"
           window_background_class="kz_window">
    <span slot="header" class="smaller"></span>
    <div slot="body">
      <div class="ugrid popbox">
        <div class="row">
          <div :class="styleclass" class="col col-12-of-12 r14basic center">
            <span class="h3">{{ $t("p_total_income") }}</span>
            <span class="mbsd ethsmall">{{ allIncomeAmount }} ETH</span>
            <span class="h3">{{ $t("p_cap") }}</span>
            <span class="mbsd ethsmall">{{ principalAmount }} ETH</span>
            <span class="h3">{{ $t("p_hack") }}</span>
            <span class="mbsd keysmall">+{{ keyAmount }}</span>
            <span class="h3">{{ $t("p_enqueue") }}排队金额</span>
            <span class="mbsd ethsmall">{{ lineAmount }} ETH</span>
            <span class="h3">{{ $t("p_shared") }} 分红总额</span>
            <span class="ethsmall mbsd">{{ dividendAmount }} ETH</span>
            <span class="h3">{{ $t("p_reward") }} 奖励总额</span>
            <span class="ethsmall mbsd">{{ recommendAmount }} ETH</span>
            <span class="h3">{{ $t("p_grant") }} 等待发放</span>
            <span class="ethsmall mbsd">{{ waitToSend }} ETH</span>
          </div>
        </div>
        <div class="row">
          <div class="col col-6-of-12 rgreybox center" @click="withdrawlbox=false">{{ $t("p_close") }}</div>
          <div class="col col-6-of-12 rgreybox center" @click="clickredraw"><span class="withdrawharvest">{{ $t("p_settle_withdraw") }}- {{ free_amount }} eth</span>
          </div>
        </div>
      </div>
    </div>
    <div slot="footer">
    </div>
  </simp-re>
</template>

<script>
import W from "Web3"
import { EventBus } from "vue-backgrounds"
import SimpRe from "../util/SimpRe"

export default {
  name: "MasonicPop",
  components: { SimpRe },
  // eslint-disable-next-line vue/require-prop-types
  props: ["styleclass"],
  data () {
    return { withdrawlbox: false }
  },
  computed: {
    principalAmount () {
      return this.$store.getters["common/principalAmount"]
    },
    free_amount () {
      return this.$store.getters["common/ready_for_withdrawal"]
    },
    allIncomeAmount () {
      return this.$store.getters["common/allIncomeAmount"]
    },
    // contract_balance
    dividendAmount () {
      return this.$store.getters["common/dividendAmount"]
    },
    recommendAmount () {
      return this.$store.getters["common/recommendAmount"]
    },
    waitToSend () {
      return this.$store.getters["common/waitToSend"]
    },
    lineAmount () {
      return this.$store.getters["common/lineAmount"]
    },
    keyAmount () {
      return this.$store.getters["common/myHackedKeyAmount"]
    }
  },
  methods: {
    clickredraw (e) {
      e.preventDefault()
      EventBus.$emit("EventUserWithdrawal")
    },
    show () {
      this.withdrawlbox = true
    },
    toEther (f) {
      return W.utils.fromWei(f + "", "ether")
    }
  }
}
</script>
