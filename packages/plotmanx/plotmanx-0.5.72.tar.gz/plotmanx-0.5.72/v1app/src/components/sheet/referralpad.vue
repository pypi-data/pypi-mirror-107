<template>
  <v-sheet outlined class="text-center holo_sheet" height="90vh">
    <v-btn class="mt-6" text color="error" @click="$emit('close')">{{ $t("p_close") }}</v-btn>
    <v-card-text>
      Please enter the referral code.
    </v-card-text>
    <input-code
      ref="pinbox"
      v-model="code"
      :length="5"
      :autofocus="false"
      placeholder="🍵"
      inputtype="referrer"
      @fillcomplete="check_valid"
    />
    <v-card-text style="color:#542929;">
      {{ result_text }}
    </v-card-text>
    <v-layout v-if="iserror || pinsuccess">
      <v-flex>
        <v-btn v-if="iserror || pinsuccess"
               :disabled="isTransactionInProcess"
               large
               class="cloux"
               @click="reset_input">try again
        </v-btn>

        <v-btn v-if="pinsuccess"
               :disabled="isTransactionInProcess"
               :loading="isTransactionInProcess"
               class="cloux"
               large
               @click="join_team">
          <!--  <v-icon>mdi-data-matrix-edit</v-icon>-->
          <v-icon>mdi-key-variant</v-icon>
          register entrance
          <template v-slot:loader>
            <span style="
                          align-items: center;
                          color: inherit;
                          display: flex;
                          flex: 1 0 auto;
                          justify-content: inherit;
                          line-height: normal;
                          position: relative;
              ">
              <v-icon>mdi-credit-card-wireless-outline</v-icon>  in process
            </span>
          </template>
        </v-btn>

        <!-- <v-btn v-if="pinsuccess" @click="see_plan">see plans</v-btn>-->
      </v-flex>
    </v-layout>
    <div class="mt-4" style="width: 200px; display: inline-block;align-items: center;">
      <Varsace name-tag="darkgold"/>
    </div>

  </v-sheet>
</template>
<script>

import { TRC975 } from "@/api/abi/trc975."
import { EventBus } from "vue-backgrounds"
import string_tx from "@/api/mixins/string_tx"
import main from "@/api/mixins/tron/main975"
import { error_explain } from "@/api/compress/error"
import { ___fromSun2Floor } from "@/api/compress/bn"
import walletx from "@/api/mixins/tron/walletx"

export default {
  name: "Referralpad",
  mixins: [main, string_tx, walletx],
  props: {
    coded: {
      type: String,
      default: "",
      required: false
    }
  },
  data: () => ({
    code: "",
    result_text: "best to have wifi",
    iserror: false,
    pinsuccess: false,
    testing_function: false,
    error_return_code: 0
  }),
  mounted() {
    this.$nextTick(() => {
      if (this.coded.length === 5) {
        this.code = this.coded
        const t = this.$refs.pinbox
        t.focusCellByIndex(4)
        t.focusNextCell()
      }
    })
  },
  methods: {
    confirmError(msg) {
      this.defaultstatus()
      const t = this.$refs.pinbox
      this.result_text = msg
      this.iserror = true
      t.setError(true)
    },
    confirmSuccess() {
      this.defaultstatus()
      this.result_text = "Lets check what's next..."
      this.pinsuccess = true
      console.log("store code:", this.code)
      this.$store.dispatch("forsage/pinned_code", this.code.toUpperCase())
    },
    defaultstatus() {
      this.pinsuccess = false
      this.iserror = false
    },
    /***
     EventBus.$on("check-code", (code) => {
        this.CheckCode(code).then((address) => {
          console.log(address)
        }).catch((e) => {
          this.notificationError(`there is an error from check the pin ${e}`)
        })
      })
     *** @param code
     */
    async check_valid(code) {
      this.result_text = "Checking please wait ..."
      const selfcode = this.$store.getters["forsage/show_invitation_code"]
      if (code === selfcode) {
        this.confirmError(`Cannot enter ${code} as this is your own invitation code.`)
        return false
      }
      if (TRC975.Instance()) {
        try {
          const result = await TRC975.Instance().isCheckCodeExist(code)
          if (!this.testing_function) {
            if (result) {
              this.confirmSuccess()
            } else {
              this.error_return_code = result
              this.confirmError(`The entered code ${code} is invalid.`)
            }
          } else {
            this.confirmSuccess()
          }
        } catch (e) {
          console.error(e)
        }
      } else {
        console.error("TRC975 instance is not found.")
      }
    },
    see_plan(e) {
      e.preventDefault()
      EventBus.$emit("check_price_plan_action")
    },
    async join_team(e) {
      e.preventDefault()
      // EventBus.$emit("price_plan_enter_deal", "", 100)
      const my_invitation_code = this.$store.getters["forsage/show_invitation_code"]
      const refer_code = this.code.toUpperCase()
      if (TRC975.Instance()) {
        try {
          const entry = this.getVal("forsage/get_min_start_ticket_price", false)
          const min_trx = this.bn2Number(entry) * 2
          const sun = this.toSun(min_trx)
          if (!this.checkIsEnough(sun)) {
            const msg = `The wallet ${___fromSun2Floor(this.coin_trx_balance)} is not enough. The entry is required at least ${entry} trx`
            this.result_text = msg
            this.notificationError(msg)
            return
          }
          this.result_text = "please wait for transaction to complete..."
          this.commitBlockTransaction()
          const bn = await TRC975.Instance().vegasRegular(my_invitation_code, refer_code, sun)
          const result = this.bn2Number(bn)
          this.releaseBlockTransaction()
          if (result === 0) {
            this.confirmSuccess()
            await this.findPlayerStatus()
          } else {
            this.confirmError(`Referral code from ${refer_code} got result ${error_explain(result)} please check with the user guide for detail.`)
            this.notificationError(error_explain(result))
            EventBus.$emit("debug_info", "entry bill", "trx", error_explain(result))
          }
        } catch (e) {
          this.releaseBlockTransaction()
          this.notificationError(e)
          EventBus.$emit("debug_info", e.error, "trx", e)
        }
      } else {
        console.error("TRC975 instance is not found.")
      }
    },
    reset_input(e) {
      e.preventDefault()
      const t = this.$refs.pinbox
      t.setError(false)
      t.reset()
      this.pinsuccess = false
      this.iserror = false
      this.result_text = ""
    }
  }
}
</script>
<style lang="scss">
@import "../../../node_modules/vue-codepin/src/presents/base";

$_inputarea: #2d3215;
$_focusborder: #7bdd16;
$_bordergrey: rgba(234, 236, 246, 0.2);
$_error_red: red;

.form-masked-pin:focus + .bg-box-group .bg-box {
  box-shadow: 0 0 0 0.15rem rgba(0, 123, 255, .25);
}

.form-masked-pin + .bg-box-group .bg-box {
  width: 14%;
  height: 65px;
  margin-top: -65px;
  display: block;
  border-radius: 3px;
  border: 1px solid #777;
  background: #fff;
}

.form-masked-pin.error + .bg-box-group + .error-msg,
.form-masked-pcolorin.fail + .bg-box-group + .error-msg {
  color: $_error_red;
  display: block;
}

.vue-pincode-input-wrapper {
  @extend .vue_input_base_wrapper;
  background: unset !important;
  margin-left: 30px;
  margin-right: 30px;

  .vue-pincode-input {
    @extend .vue_input_base;
    background: $_inputarea;
    border: 0.5px solid $_bordergrey;
    text-transform: uppercase;
    font-family: "varsace", 'Open Sans', Arial, sans-serif;

    &:focus {
      box-shadow: 0 0 0 0.15rem $_focusborder;
    }
  }

  &.v-pin-error .vue-pincode-input {
    box-shadow: 0 0 0 0.15rem $_error_red;
  }
}

</style>
