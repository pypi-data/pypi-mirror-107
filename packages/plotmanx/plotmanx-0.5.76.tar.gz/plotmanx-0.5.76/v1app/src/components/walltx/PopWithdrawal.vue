<template>
  <simp-re v-if="withdrawlbox"
           window_mask="std_window_mask"
           class="windowed_table_x"
           window_background_class="kz_window">
    <span slot="header" class="smaller"></span>
    <div slot="body">
      <div class="ugrid popbox">
        <div class="row">
          <div class="col col-6-of-12 r12basic center">
            <span class="h3">Total Income</span>
            <span class="mbsd iconeth">{{ allIncomeAmount }} ETH</span>
            <p>财富自由</p>
          </div>
          <div class="col col-6-of-12 r13basic center" @click="clickredraw">
            <span class="h3">Capital</span>
            <p>小额投资</p>
            <span class="mbsd iconeth">{{ principalAmount }} ETH</span>
            <p>Withdraw</p>
          </div>
        </div>

        <div class="row">
          <div class="col col-6-of-12 r12basic center">
            <span class="h3">Waiting Amount 排队金额</span>
            <span class="iconeth mbsd">{{ lineAmount }} ETH</span>
            <p>排队</p>
          </div>
          <div class="col col-6-of-12 r14basic center">
            <span class="h3">Shared Amount 分红总额</span>
            <span class="iconeth mbsd">{{ dividendAmount }} ETH</span>
            <p>不断积累</p>
          </div>
        </div>

        <div class="row">
          <div class="col col-6-of-12 r12basic center">
            <span class="h3">Reward Amount 奖励总额</span>
            <span class="iconeth mbsd">{{ recommendAmount }} ETH</span>
            <p>分享的力量</p>
          </div>
          <div class="col col-6-of-12 r11basic center">
            <span class="h3">Queued Delivery 等待发放</span>
            <span class="iconeth mbsd">{{ waitToSend }} ETH</span>
            <p>至少0.1ETH</p>
          </div>
        </div>
        <div class="row">
          <div class="col col-6-of-12 rgreybox center" @click="withdrawlbox=false">X CLOSE</div>
          <div class="col col-6-of-12 rgreybox center" @click="clickredraw">V WITHDRAW</div>
        </div>
      </div>
    </div>
    <div slot="footer">
    </div>
  </simp-re>
</template>
<script>
import W from "Web3"
import SimpRe from "../util/SimpRe"

export default {
  name: "PopFwWithdrawal",
  components: { SimpRe },
  data () {
    return { withdrawlbox: false }
  },
  computed: {
    principalAmount () {
      return this.$store.getters["fw/principalAmount"]
    },
    allIncomeAmount () {
      return this.$store.getters["fw/allIncomeAmount"]
    },
    // contract_balance
    dividendAmount () {
      return this.$store.getters["fw/dividendAmount"]
    },
    recommendAmount () {
      return this.$store.getters["fw/recommendAmount"]
    },
    waitToSend () {
      return this.$store.getters["fw/waitToSend"]
    },
    lineAmount () {
      return this.$store.getters["fw/lineAmount"]
    }
  },
  methods: {
    clickredraw (e) {
      e.preventDefault()
      this.$emit("EventUserWithdrawal")
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
