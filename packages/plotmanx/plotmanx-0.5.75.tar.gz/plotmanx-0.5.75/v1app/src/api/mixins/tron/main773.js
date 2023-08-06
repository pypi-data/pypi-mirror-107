/*

 */
import { TRC773 } from "@/api/abi/trc773."
import wallex from "@/api/mixins/tron/walletx"
import nav from "@/api/mixins/tron/nav"
import { txtUnit } from "@/api/compress/bn"
import { EventBus } from "vue-backgrounds"
import { getStoredItemInt } from "@/api/compress/urltool"
import { generateHashDraw, hit } from "@/api/compress/algokeno"

export default {
  mixins: [wallex, nav],
  computed: {
    block_time_last_update() {
      return this.$store.getters["keno/block_time_last_update"]
    },
    banker_locked_fund() {
      return this.$store.getters["keno/g_banker_locked_fund"]
    },
    banker_fund() {
      return this.$store.getters["keno/g_banker_fund"]
    },
    roulette_num() {
      return this.$store.getters["keno/g_roulette_number"]
    },
    timeout_reveal() {
      return this.$store.getters["keno/g_timeout"]
    },
    management_fund() {
      return this.$store.getters["keno/g_management_fee"]
    },
    round_number() {
      return this.$store.getters["keno/r"]
    },
    remain_time() {
      return this.$store.getters["keno/remain_t"]
    },
    ticket_no() {
      return this.$store.getters["keno/tktid"]
    },
    pocket_fund() {
      return this.$store.getters["keno/pocket_fund"]
    },
    user_value() {
      return this.$store.getters["keno/user_value"]
    },
    gg_result() {
      return this.$store.getters["keno/gg_result"]
    },
    gg_block() {
      return this.$store.getters["keno/gg_block"]
    },
    user_bet_on() {
      return this.$store.getters["keno/user_bet_on"]
    },
    sum_investors() {
      return this.$store.getters["keno/show_investors"]
    },
    cannot_purchase() {
      const { purchase } = this.$store.getters["keno/flags_state"]
      return !purchase
    },
    cannot_draw() {
      const { draw } = this.$store.getters["keno/flags_state"]
      return !draw
    },
    post_bet() {
      return txtUnit(this.$store.getters["keno/time_post_secret"])
    },
    last_play() {
      return txtUnit(this.$store.getters["keno/time_last_play"])
    },
    max_bet() {
      return Math.min(txtUnit(this.pocket_fund), txtUnit(this.banker_fund)) * 0.5
    },
    userRegistered() {
      return this.$store.getters["keno/show_in_game"]
    },
    bank_fund() {
      return this.$store.getters["keno/show_bank"]
    },
    ui_disabled() {
      const { state } = this.statusGen()
      return state === 5 || state === 1 || state === 2 || state === 4
    },
    bet_button_disabled() {
      const { bool } = this.statusGen()
      const { bet_sub } = this.$store.getters["keno/flags_state"]
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
      check_looper: 0,
      factors: []
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
      const { betlock, draw, purchase } = this.$store.getters["keno/flags_state"]
      if (purchase) {
        if (betlock) {
          if (draw) {
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
        } else if (draw) {
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
    async setlist(list) {
      await this.$store.dispatch("keno/lotto_picks", list)
      this.factors = hit(list.length)
    },
    async snap_draw() {
      const _that = this
      if (_that.is_contract_ready()) {
        const contract = TRC773.Instance()
        const static_func = {
          signer(payload) {
            _that.report_event(payload)
            _that.notificationInfo(`The new bet uuid ${payload.uuid}`)

            return true
          },
          reply(payload) {
            const checker_t = payload.data.txID
            _that.notificationInfo(`The broadcast transaction uuid ${checker_t}`)
            if (localStorage) {
              localStorage.setItem("v773_checker_time", String(checker_t))
            }
            return true
          },
          debug(message) {
            _that.report_debug(message)
            return true
          }
        }
        _that.tronLink.setCallbackFunctionCall("drawWin(bytes32)", static_func)
        const hash = generateHashDraw()
        console.log(hash)
        try {
          await contract.drawWin(hash)
        } catch (e) {
          this.report_error(e)
        }
      } else {
        this.report_error("instance TRC733 is not init.")
      }
    },
    require_initial_instance_TRC773() {
      return this.tronWeb && !TRC773.Instance()
    },
    r_contract_ready() {
      return !!TRC773.Instance()
    },
    async contract_init() {
      if (!TRC773.Instance()) {
        try {
          const defined_contract = new TRC773(this.tronWeb)
          defined_contract.setDebug(false)
          this.loading_message("bind contract")
          await defined_contract.init(process.env.c773)
        } catch (e) {
          this.report_error(e)
        }
      }
    },
    /**
     * update player info by the address
     * @returns {Promise<void>}
     */
    async findPlayerStatus() {
      try {
        this.loading_message("read block player data")
        const customer_data = await TRC773.Instance().yokohama()
        if (this.isDebug()) {
          console.group("yokohama data ==> ")
          console.log(customer_data)
          console.groupEnd()
        }
        await this.$store.dispatch("keno/ylo_player_matrix", customer_data)
      } catch (e) {
        this.report_error_trn(e, "account wallet")
      }
    },
    async first_check_last_block_price(contract) {
      const timer = getStoredItemInt("v773_checker_time", 0)
      this.loading_message(`last block message since: ${timer}`)
      let result = await contract.eventQ("GameResult", 0, timer)
      result = contract.sortEventsDescending(result)
      if (result.length > 0) {
        await this.$store.dispatch("keno/record_last", result[0])
      }
    },
    is_contract_ready() {
      return !!TRC773.Instance()
    },
    /**
     * this is the system status
     * @returns {Promise<void>}
     */
    async systemStatus() {
      try {
        this.loading_message("read block data")
        const system_updated = await TRC773.Instance().shenzhen()
        /** ====
         console.group("paris sys update data ==> ")
         console.log(system_updated)
         console.groupEnd()
         ***/
        await this.$store.dispatch("keno/shenzhen", system_updated)
      } catch (e) {
        this.report_error_trn(e, "sys dat")
      }
    },
    /**
     * info basic contracts
     * @returns {Promise<void>}
     */
    async contract_scan(notLogin) {
      this.event_loading_process(true)
      if (this.tronLink.isLoggedIn()) {
        await this.findPlayerStatus()
      } else {
        console.log("tron wallet is not login")
        if (notLogin) {
          notLogin()
        }
      }
      if (this.is_contract_ready()) {
        await this.systemStatus()
        // await this.GetPriceLimit()
        // await this.DetermineUserInGame()
        this.my_invitation_code = this.$store.getters["keno/show_invitation_code"]
        //  await this.getLevelByActive()
      } else {
        console.log("contract is not init")
      }
      this.event_loading_process(false)
    }
  }
}
