<template>
  <div class="col col-12-of-12 r16basic center statusboxspecial">
    <div :class="{disabled: cooldown>0}" class="bxxx">
      <span :style="{width: cooldown + '%'}" class="cool_cp_down"></span>
      <div class="bpsee">
        <span class="typed3">{{ $t("bnt_trxn") }}</span>
        <span class="typed3">{{ data_transaction }}</span>
      </div>
    </div>
  </div>
</template>
<script>
import { TimelineLite } from "gsap"

export default {
  name: "StatusBox",
  data() {
    return {
      data_transaction: "",
      cooldown: 0
    }
  },
  mounted() {
    const timelineLip = new TimelineLite()
    this.$GSLite = timelineLip
  },
  methods: {
    demo() {
      this.cdown()
    },
    MakeNewHash(hash) {
      this.data_transaction = hash
      this.cdown()
    },
    ConfirmTransactions(hash) {
      this.data_transaction = this.$t("n_hashcfm") + ": " + hash
    },
    Denied() {
      this.data_transaction = this.$t("n_deny")
    },
    cdown() {
      console.log("cd down is now")
      const that = this
      if (that.cooldown === 0) {
        that.cooldown = 100
        that.$GSLite.to(that, 18, { cooldown: 0 })
        that.$GSLite.eventCallback("onComplete", that.cdownComplete)
      }
    },
    cdownComplete() {
      // when all checkers are completed
      /* this.$emit ("invest_submission", {
           amount : parseFloat (this.bet_amount),
           currency : this.coin_symbol,
           invite_code : this.invite_code,
           time : new Date ()
         }); */
    }
  }
}
</script>
<style scoped lang="scss">
$colorUp: #7bfa94;
$colorDown: #28973a;
$color10Down: #1e702b;
$color11Down: #103b17;
.bxxx {
  margin: 0;
  background: linear-gradient(-135deg, $color10Down 0%, $color11Down 100%);
  padding: 50px;
  display: block;
  position: relative;

  .cool_cp_down {
    position: absolute;
    height: 100%;
    background: linear-gradient(-135deg, $colorUp 0%, $colorDown 100%);
    left: 0;
    bottom: 0;
    z-index: 2;
  }

  .bpsee {
    top: 0px;
    left: 0px;
    width: 100%;
    position: absolute;
    z-index: 3;
  }
}

.statusboxspecial {
  padding: 0px;
  overflow: hidden;
  border: 1px solid $colorDown;
}
</style>
