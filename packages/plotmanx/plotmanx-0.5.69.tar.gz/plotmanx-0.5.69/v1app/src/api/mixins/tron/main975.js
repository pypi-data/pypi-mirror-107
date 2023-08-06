import { EventBus } from "vue-backgrounds"
import { TRC975 } from "@/api/abi/trc975."
import wallex from "@/api/mixins/tron/walletx"

export default {
  mixins: [wallex],
  computed: {
    isTransactionInProcess() {
      return this.$store.getters["forsage/show_block_in_process"]
    },
    userRegistered() {
      return this.$store.getters["forsage/show_in_game"]
    },
    bank_fund() {
      return this.$store.getters["forsage/show_bank"]
    },
    my_earning() {
      return this.$store.getters["forsage/show_earning"]
    },
    sum_investors() {
      return this.$store.getters["forsage/show_investors"]
    }
  },
  data() {
    return {
      founder: "",
      tokenName: "",
      sTranferExpressReceipt: "",
      amount: 0,
      confirmations: 0,
      contract_address: "",
      copy__: "",
      iamVIP: false,
      process_t0: false,
      process_f1: false,
      process_f2: false,
      process_f3: false,
      process_f4: false,
      clipboard: false,
      isRoundNOTStarted: false,
      checked_time: 0
    }
  },
  methods: {
    async contract_init() {
      if (!TRC975.Instance()) {
        try {
          const defined_contract = new TRC975(this.tronWeb)
          defined_contract.setDebug(false)
          this.loading_message("bind contract")
          await defined_contract.init(process.env.c975)
          /**
           await defined_contract.startEventListeners()
           defined_contract.on("event_MissedEthReceive", (d) => {
            EventBus.$emit("event_MissedEthReceive", d)
          })
           defined_contract.on("event_NewUserPlace", (d) => {
            EventBus.$emit("event_NewUserPlace", d)
          })
           defined_contract.on("event_Registration", (d) => {
            EventBus.$emit("event_Registration", d)
          })
           defined_contract.on("event_Reinvest", (d) => {
            EventBus.$emit("event_Reinvest", d)
          })
           defined_contract.on("event_SentExtraEthDividends", (d) => {
            EventBus.$emit("event_SentExtraEthDividends", d)
          })
           defined_contract.on("event_Upgrade", (d) => {
            EventBus.$emit("event_Upgrade", d)
          }) */
        } catch (e) {
          this.report_error(e)
        }
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
        this.my_invitation_code = this.$store.getters["forsage/show_invitation_code"]
        //  await this.getLevelByActive()
      } else {
        console.log("contract is not init")
      }
      this.event_loading_process(false)
    },
    is_contract_ready() {
      return !!TRC975.Instance()
    },
    checkTrxLx() {
    },
    /**
     * this is the system status
     * @returns {Promise<void>}
     */
    async systemStatus() {
      try {
        this.loading_message("read block data")
        const system_updated = await TRC975.Instance().paris()
        /** ====
         console.group("paris sys update data ==> ")
         console.log(system_updated)
         console.groupEnd()
         ***/
        this.saveLocal("forsage/parisLos", system_updated)
      } catch (e) {
        this.report_error_trn(e, "sys dat")
      }
    },
    /**
     * update player info by the address
     * @returns {Promise<void>}
     */
    async findPlayerStatus() {
      try {
        this.loading_message("read block player data")
        const customer_data = await TRC975.Instance().yokohama()
        if (this.isDebug()) {
          console.group("yokohama data ==> ")
          console.log(customer_data)
          console.groupEnd()
        }
        this.saveLocal("forsage/player_imatrix", customer_data)
      } catch (e) {
        this.report_error_trn(e, "account wallet")
      }
    },
    async getLevelByActive() {
      let L = 1
      try {
        while (L < 12) {
          const address = this.tronLink.getAccountAddress()
          const x3 = await TRC975.Instance().usersActiveX3Levels(address, L)
          const x6 = await TRC975.Instance().usersActiveX6Levels(address, L)
          // console.log(x3, x6)
          const ex = {
            lv: L,
            x3,
            x6
          }
          this.saveLocal("forsage/store_level", ex)
          L++
        }
        console.log("level by active")
      } catch (e) {
        this.report_scan_error(e)
      }
    },
    /**
     * get the price plan
     * @returns {Promise<void>}
     * @constructor
     */
    async GetPriceLimit() {
      try {
        const info = await TRC975.Instance().rome()
        this.saveLocal("forsage/level_price", info)
      } catch (e) {
        this.report_error_trn(e, "account price list")
      }
    },
    async GetLevelInfod() {
      try {
        if (!this.userRegistered) {
          return
        }
        const info = await TRC975.Instance().fukuoka()
        if (this.isDebug()) {
          console.group("GetPriceLimit data ==> ")
          console.log(info)
          console.groupEnd()
        }
        // this.saveLocal("forsage/level_info", info)
      } catch (e) {
        this.report_error_trn(e, "account fukuoka")
      }
    },
    /**
     * determine if the player is already registered in the game
     * @returns {Promise<void>}
     * @constructor
     */
    async DetermineUserInGame() {
      const in_code = this.$store.getters["forsage/show_invitation_code"]
      const inGame = await TRC975.Instance().isCheckCodeExist(in_code)
      this.saveLocal("forsage/player_ingame", inGame)
    },
    getReferText() {
      return this.myinvitationcode
    },
    commitBlockTransaction() {
      this.saveLocal("forsage/in_block_transaction", true)
    },
    releaseBlockTransaction() {
      this.saveLocal("forsage/in_block_transaction", false)
    }
  }
}
