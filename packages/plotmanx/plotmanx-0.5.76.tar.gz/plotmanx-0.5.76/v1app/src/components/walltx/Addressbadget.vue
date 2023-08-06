<template>
  <div class="row hash_area">
    <div class="col col-4-of-12">
      <div :class="healthcheckclass" class="statusLight">[{{ class_signal_count }}]</div>
    </div>
    <div class="col col-8-of-12">
      <a :href="contract_link" target="_blank"><span>{{ display_address }}</span></a>
    </div>
  </div>
</template>
<script>
export default {
  name: "AddressBadget",
  computed: {
    display_address () {
      return `${this.$t("msg_verified_ctr")}: ${this.contract_address}`
    },
    healthcheckclass () {
      // sync_health
      return this.$store.getters["wallet/sync_health"] ? "health" : "sick"
    },
    class_signal_count () {
      return this.$store.getters["wallet/inSyncs"]
    },
    contract_address () {
      return this.$store.getters["wallet/addressContract"]
    },
    contract_link () {
      const net = this.$store.getters["wallet/network"]
      // return `https://${net}.etherscan.io/verifyContract?a=${this.contract_address}`;
      // https://rinkeby.etherscan.io/address/0x416Df61ee012749f566106275d5847Df4f046BDd
      return `https://${net}.etherscan.io/address/${this.contract_address}`
    }
  }
}
</script>
