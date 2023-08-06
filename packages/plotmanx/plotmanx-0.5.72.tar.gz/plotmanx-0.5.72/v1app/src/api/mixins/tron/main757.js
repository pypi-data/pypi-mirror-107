import { TRC757 } from "@/api/abi/trc757."
import wallex from "@/api/mixins/tron/walletx"
import nav from "@/api/mixins/tron/nav"
import { ___fromSun, txtUnit } from "@/api/compress/bn"
import { EventBus } from "vue-backgrounds"
import { getStoredItemInt } from "@/api/compress/urltool"

export default {
  mixins: [wallex, nav],
  computed: {
    block_time_last_update() {
      return this.$store.getters["roulette/block_time_last_update"]
    },
    banker_locked_fund() {
      return this.$store.getters["roulette/g_banker_locked_fund"]
    },
    banker_fund() {
      return this.$store.getters["roulette/g_banker_fund"]
    },
    roulette_num() {
      return this.$store.getters["roulette/g_roulette_number"]
    },
    timeout_reveal() {
      return this.$store.getters["roulette/g_timeout"]
    },
    management_fund() {
      return this.$store.getters["roulette/g_management_fee"]
    },
    bank_hash() {
      return this.$store.getters["roulette/bank_hash"]
    },
    pocket_fund() {
      return this.$store.getters["roulette/pocket_fund"]
    },
    locked_fund() {
      return this.$store.getters["roulette/locked_fund"]
    },
    user_value() {
      return this.$store.getters["roulette/user_value"]
    },
    bank_secret() {
      return this.$store.getters["roulette/bank_secret"]
    },
    gg_result() {
      return this.$store.getters["roulette/gg_result"]
    },
    gg_block() {
      return this.$store.getters["roulette/gg_block"]
    },
    user_bet_on() {
      return this.$store.getters["roulette/user_bet_on"]
    },
    already_initialized() {
      const { requested } = this.$store.getters["roulette/flags_interpret"]
      return requested
    },
    system_in_rgam() {
      const { play } = this.$store.getters["roulette/yf_flags"]
      return play
    },
    post_bet() {
      return txtUnit(this.$store.getters["roulette/time_post_secret"])
    },
    last_play() {
      return txtUnit(this.$store.getters["roulette/time_last_play"])
    },
    max_bet() {
      return Math.min(txtUnit(this.pocket_fund), txtUnit(this.banker_fund)) * 0.5
    },
    cash_out_button_disable() {
      const { value } = this.$store.getters["roulette/flags_interpret"]
      const in_game_op = this.system_in_rgam
      if (value || in_game_op) {
        return true
      } else {
        return false
      }
    },
    ui_disabled() {
      const { state } = this.statusGen()
      return state === 5 || state === 1 || state === 2 || state === 4
    },
    bet_button_disabled() {
      const { bool } = this.statusGen()
      const { bet_sub } = this.$store.getters["roulette/yf_flags"]
      return bool || bet_sub
    },
    bet_button_label() {
      const { val } = this.statusGen()
      return val
    }
  },
  data() {
    return {
      bet_on_red: false,
      bet_amount_for_roulette_pv: 0,
      check_looper: 0
    }
  },
  mounted() {
    this.$on("notify_tron_opensign", this.signOpen)
  },
  beforeDestroy() {
    clearInterval(this.check_looper)
  },
  methods: {
    signOpen() {

    },
    statusGen() {
      const { value, hash, requested } = this.$store.getters["roulette/flags_interpret"]
      if (requested) {
        if (value) {
          if (hash) {
            return {
              bool: true,
              val: "waiting the result",
              state: 1
            }
          } else {
            return {
              bool: true,
              val: "n/a",
              state: 2
            }
          }
        } else if (hash) {
          return {
            bool: false,
            val: "confirm bet",
            state: 3
          }
        } else {
          return {
            bool: true,
            val: "waiting to confirm",
            state: 4
          }
        }
      } else {
        return {
          bool: false,
          val: "request bet",
          state: 5
        }
      }
    },
    require_initial_instance_trc757() {
      return this.tronWeb && !TRC757.Instance()
    },
    r_contract_ready() {
      return !!TRC757.Instance()
    },
    roll_start() {
      this.notificationWarning("The account is now locked for the roll, good luck! Do not close this app.")
      this.$store.dispatch("roulette/yf_start_flag", true)
    },
    roll_done() {
      this.info_sphere()
      this.notificationSuccess("Rolling done.")
      this.$store.dispatch("roulette/yf_start_flag", false)
    },
    async started_roll() {
      const _that = this
      this.debugTronLink(true)
      if (_that.Check757Instance()) {
        return
      }
      const contract = TRC757.Instance()
      if (_that.system_in_rgam) {
        return
      }
      const { state } = _that.statusGen()
      if (___fromSun(_that.pocket_fund) < 50) {
        this.notificationError("You do not have enough fund in the pocket. Please make at least 50 trx to the pocket.")
        return
      }
      if (state === 5) {
        await contract.initializeGame()
        return
      }
      if (_that.bet_amount_for_roulette_pv === 0) {
        this.notificationError("Please make place a bet")
        return
      }
      if (state === 3) {
        if (_that.bet_amount_for_roulette_pv > 10) {
          const update_time = new Date()
          const checker_t = Math.floor(update_time.getTime())

          const static_func = {
            signer(payload) {
              _that.report_event(payload)
              _that.notificationInfo(`The new bet uuid ${payload.uuid}`)
              _that.$store.dispatch("roulette/yf_bet_sub", true)
              return true
            },
            reply(payload) {
              _that.notificationInfo(`The broadcast transaction uuid ${payload.data.txID}`)
              if (localStorage) {
                localStorage.setItem("v757_checker_time", String(checker_t))
              }

              EventBus.$emit("reel_roll_state_check")
              _that.loop_check_result(contract, checker_t, _that.tronLink.getAccountAddress0x())

              setTimeout(async () => {
                await _that.info_sphere()
                await _that.first_check_last_block_price(contract)
              }, 5000)

              return true
            },
            debug(message) {
              _that.report_debug(message)
              return true
            }
          }

          const nonce = Math.floor(Math.random() * update_time.getMilliseconds())
          const sun = _that.toSun(_that.bet_amount_for_roulette_pv)
          _that.tronLink.setCallbackFunctionCall("placeBet(bool,uint256,uint256)", static_func)
          try {
            await contract.placeBet(_that.bet_on_red, nonce, sun)
          } catch (e) {
            await _that.$store.dispatch("roulette/yf_bet_sub", false)
            _that.tronLink.removeAllFunctionCalls()
            _that.report_error_trn(e, "bet")
          }
        } else {
          _that.notificationError(`Make sure the status is now with bet at least 10 trx. Now ${_that.bet_amount_for_roulette_pv}`)
        }
      }
      this.debugTronLink(false)
    },
    loop_check_result(contract, since, player_address) {
      this.check_looper = setInterval(async () => {
        const result = await contract.eventQ("GameResult", 0, since)
        if (Array.isArray(result)) {
          this.notificationInfo("checking the blockchain prize result.")
          const result_list = _.filter(contract.sortEventsDescending(result), ["result.user", player_address])
          if (result_list.length > 0) {
            const last = result_list[0]
            console.log(last, player_address)
            if (last.hasOwnProperty("result")) {
              console.log("has the result with number", last.result)
              await this.$store.dispatch("roulette/yf_bet_sub", false)
              EventBus.$emit("reel_roll_callback_result", parseInt(last.result.result))
            }
            clearInterval(this.check_looper)
          }
        } else {
          this.report_error(`Now it is up on the result - ${result} and ${since}`)
        }
      }, 10000)
    },
    async contract_roulette_init(done) {
      this.loading_message("check facility")
      if (this.tronWeb) {
        if (!TRC757.Instance()) {
          try {
            this.loading_message("contract binding")
            const defined_contract = new TRC757(this.tronWeb)
            defined_contract.setDebug(false)
            await defined_contract.init(process.env.c757)
            this.loading_message("contract binding success")
            this.rx_status_checker(defined_contract)
            await this.first_check_last_block_price(defined_contract)
          } catch (e) {
            this.loading_message("initialize error")
            this.report_error(e.toString())
          } finally {
            done()
          }
        } else {
          try {
            const ctc = TRC757.Instance()
            await this.info_sphere()
            this.rx_status_checker(ctc)
            await this.first_check_last_block_price(ctc)
          } catch (e) {
            this.loading_message("reinit error")
            this.report_error(e.toString())
          } finally {
            done()
          }
        }
      } else {
        this.report_error("contract is not init for the roulette")
        console.log("continue the contract is not init")
      }
    },
    async first_check_last_block_price(contract) {
      const timer = getStoredItemInt("v757_checker_time", 0)
      this.loading_message(`last block message since: ${timer}`)
      let result = await contract.eventQ("GameResult", 0, timer)
      result = contract.sortEventsDescending(result)
      if (result.length > 0) {
        await this.$store.dispatch("roulette/record_last", result[0])
      }
    },
    rx_status_checker(contract) {
      this.loading_message("event checker")
      const { state } = this.statusGen()
      console.log("my status", state)
      if (state === 1) {
        this.loading_message("reel_roll_state_check")
        const timer = getStoredItemInt("v757_checker_time", 0)
        console.log("check since:", timer)
        this.loop_check_result(contract, timer, this.tronLink.getAccountAddress0x())
      }
    },
    /**
     * info basic contracts
     * @returns {Promise<void>}
     */
    async game_system_scan() {
      if (!this.tronLink.isLoggedIn()) {
        console.log("tron wallet is not login")
        return
      }
      this.event_loading_process(true)
      if (this.r_contract_ready()) {
        if (!this.system_in_rgam) {
          await this.info_sphere()
        }
      }
      this.event_loading_process(false)
    },
    async info_sphere() {
      if (this.Check757Instance()) {
        return
      }
      this.loading_message("reading block data")
      const dat = await TRC757.Instance().sphere_x()
      if (this.isDebug()) {
        console.group("shenzhen data ==> ")
        console.log(dat)
        console.groupEnd()
      }
      await this.$store.dispatch("roulette/shenzhen", dat)
    }
  }
}
