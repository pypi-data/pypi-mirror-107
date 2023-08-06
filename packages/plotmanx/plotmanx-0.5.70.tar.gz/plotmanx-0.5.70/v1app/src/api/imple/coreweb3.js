// import ERC20 from "../../assets/abi/erc20";
import Clip from "clipboard"

export default {
  computed: {
    isFounder() {
      return this.$store.getters["wallet/isFounder"]
    },
    isPerm() {
      return this.$store.getters["wallet/isPermissioned"]
    },
    isLogin() {
      return this.$store.getters["wallet/isLoginWeb3"]
    },
    inception_wallet_status() {
      return this.$store.getters["wallet/wallet_setup"]
    },
    tokenList() {
      return this.$store.getters["wallet/user_tokens"]
    },
    class_hash_approval() {
      if (this.token_send_approval_hash.length > 0) {
        const index = this.txHashToIndex[this.token_send_approval_hash]
        if (this.txs[index].status === "mined") {
          return "is-success"
        } else if (this.txs[index].status === "error") {
          return "is-err"
        } else {
          return "is-progress"
        }
      } else {
        return "hide"
      }
    },
    wallet_coin() {
      return this.$store.getters["wallet/QueryNowBalance"]
    },
    coin_symbol() {
      return this.$store.getters["wallet/QueryNowSymbol"]
    },
    contractAddress() {
      return this.$store.getters["wallet/addressContract"]
    },
    mywalletaddress() {
      return this.$store.getters["wallet/user_account"]
    },
    contractBalance() {
      return this.$store.getters["wallet/QueryContractBalance"]
    }
  },
  data() {
    return {
      contractInstance: "",
      txObject: {},
      basicOptions: {},
      W3: "",
      ABI: "",
      networkName: "",
      txs: [],
      txHashToIndex: [],
      token_send_approval_hash: ""
    }
  },
  methods: {
    isAddressH(t) {
      return this.W3.utils.isAddress(t)
    },
    toEther(num) {
      return this.W3.utils.fromWei(num + "", "ether")
    },
    toHex(num) {
      return this.W3.utils.toHex(num)
    },
    toBN(num) {
      return this.W3.utils.toBN(num)
    },
    toWei(num) {
      return this.W3.utils.toWei(num, "ether")
    },
    toWeiBN(num) {
      return this.W3.utils.toBN(this.toWei(num))
    },
    /**
     * todo: fix the calculations
     * @param val
     * @param decimals_x
     * @returns {BN | *}
     */
    toTokenVal(val, decimals_x) {
      const d = 18 - decimals_x
      if (d === 0) {
        const te = this.toWei(val)
        console.log(te)
        return te
      } else {
        const f = this.toBN(10).pow(d)
        const wefi = this.toWei(val)
        console.log(wefi)
        const u = this.toBN(wefi).div(f)
        return u
      }
    },
    toTokenValWei(val, decimals_x) {
      const base = this.toBN(10).pow(this.toBN(decimals_x))
      const dm = this.toBN(val).divmod(base)
      return dm.div + "." + dm.mod.toString(10, decimals_x)
    },
    toTokenValWeiF4(val, decimals_x) {
      const f = 10 ** Number(decimals_x)
      const g = Number(val) / f
      return Number(g).toFixed(4)
    },
    showBalanceFromApiEthScout(stardard_data) {
      if (stardard_data.add === "0x0") {
        return this.toEther(stardard_data.bal)
      } else {
        console.log(stardard_data.bal, stardard_data.deci)
        return this.toTokenValWeiF4(stardard_data.bal, stardard_data.deci)
      }
    },
    async RegisterContractEvent(eventName) {
      const b = await this.W3.eth.getBlockNumber()
      const latest = b - 1
      const th = this
      return this.contractInstance.events[eventName]({
        fromBlock: this.toHex(latest),
        toBlock: "latest"
      }, function (error, event) {
        console.log("result:\n" + JSON.stringify(event))
      }).on("data", function (event_data) {
        th.$emit(eventName, event_data)
      }).on("changed", function (event_data) {
        th.$emit(eventName + "_ch", event_data)
        // remove event from local database
      }).on("error", console.error)
    },
    async InvokeGetFunction(functionName, params) {
      const account = this.$store.getters["wallet/user_account"]
      // console.log (this.contractInstance);
      return await this.contractInstance.methods[functionName](...params).call({ from: account })
    },
    async InvokeGetFunc(functionName) {
      const account = this.$store.getters["wallet/user_account"]
      // console.log (this.contractInstance);
      return await this.contractInstance.methods[functionName]().call({ from: account })
    },
    InvokeFunctionCoinSend(functionName, params) {
      //    gas : this.toHex (gas_price + 150000) }
      const currentAccount = this.$store.getters["wallet/user_account"]
      /* const ev = this.CalculateCallGas (functionName, params, (gas_price) => {
         console.log ("gas:", gas_price);
       });
       return ev; */
      return this.contractInstance.methods[functionName](...params)
        .send({
          from: currentAccount,
          to: this.contractAddress,
          gas: 6500000
        })
        .on("transactionHash", function (hash) {
          console.log("hash gen", hash)
        })
        .on("confirmation", (confirmationNumber, receipt) => {
          console.log("confirmation gen", receipt)
        })
        .on("receipt", function (receipt) {
          console.log("receipt gen", receipt) // 查询这里可以得到结果
        })
        .on("error", function (e) {
          console.error(e)
        })
    },
    InvokeFunctionEtherCallSend(amount, functionName) {
      const currentAccount = this.$store.getters["wallet/user_account"]
      return this.contractInstance.methods[functionName]()
        .send({
          from: currentAccount,
          value: this.toWei(String(amount)),
          to: this.contractAddress
        })
        .on("transactionHash", function (hash) {
          console.log("hash gen", hash)
        })
        .on("confirmation", (confirmationNumber, receipt) => {
          console.log("confirmation gen", receipt)
        })
        .on("receipt", function (receipt) {
          // receipt example
          console.log("receipt gen", receipt) // 查询这里可以得到结果
        })
        .on("error", function (e) {
          console.error(e)
        })
    },
    InvokeFunctionEtherSend(amountEther, functionName, params) {
      const currentAccount = this.$store.getters["wallet/user_account"]
      return this.contractInstance.methods[functionName](...params)
        .send({
          from: currentAccount,
          value: this.toWei(String(amountEther)),
          to: this.contractAddress
        })
        .on("transactionHash", function (hash) {
          console.log("hash: function", functionName, hash)
        })
        .on("confirmation", (confirmationNumber, receipt) => {
          console.log("confirmation: function", functionName, receipt)
        })
        .on("receipt", function (receipt) {
          // receipt example
          console.log("receipt: function", functionName, receipt) // 查询这里可以得到结果
        })
        .on("error", function (e) {
          console.error(e)
        })
    },
    InvokeWriteFunc(functionName, params) {
      const currentAccount = this.$store.getters["wallet/user_account"]
      return this.contractInstance.methods[functionName](...params)
        .send({ from: currentAccount })
        .on("transactionHash", function (hash) {
          console.log("hash gen", hash)
        })
        .on("confirmation", (confirmationNumber, receipt) => {
          console.log("confirmation gen", receipt)
        })
        .on("receipt", function (receipt) {
          console.log("receipt gen", receipt) // 查询这里可以得到结果
        })
        .on("error", function (e) {
          console.error(e)
        })
    },
    async getTxStatus(hash) {
      // console.log ("GET TX STATUS", hash);
      if (!this.process_f4) {
        return
      }
      // console.log ("again to check.");
      setTimeout(() => {
        this.W3.eth.getTransactionReceipt(hash, (error, res) => {
          if (res && res.blockNumber) {
            if (res.status) {
              const index = this.txHashToIndex[hash]
              this.txs[index].status = "mined"
              // console.log ("GET TX STATUS MINDED", hash);
            } else {
              const msg = "Mined but with errors. Perhaps out of gas"
              const index = this.txHashToIndex[hash]
              this.txs[index].status = "error"
              this.txs[index].name = msg
              // console.log ("GET TX STATUS ERROR", this.txs[index]);
              this.notificationError(msg)
              this.process_f4 = false
            }
          } else {
            this.getTxStatus(hash)
          }
          //  console.log (res);
        })
      }, 3000)
    },
    async dec(tokenAddress) {
      // console.log (ERC20);
      const token = await new this.W3.eth.Contract(ERC20, tokenAddress)
      return await token.methods.decimals().call()
    },
    async _approve(tokenAddress, token_amount, decimal, symbol) {
      const index = this.txs.length
      const token = await new this.W3.eth.Contract(ERC20, tokenAddress)
      this.token_send_approval_hash = ""
      const approve_amount = this.toTokenVal(token_amount, decimal)
      console.log("token amount to approved: ", approve_amount)
      // let result_unlocked = token.methods["approve"] (this.contractAddress, String(approve_amount))
      const result_unlocked = token.methods.approve(this.contractAddress, approve_amount)
        .send({ from: this.mywalletaddress })
        .on("transactionHash", (hash) => {
          this.token_send_approval_hash = hash
          this.txHashToIndex[hash] = index
          this.txs[index] = {
            status: "pending",
            name: `GroupSend Approval to spend ${token_amount} ${symbol}`,
            hash
          }
          this.getTxStatus(hash)
        })
        .on("error", (error) => {
          console.error(error)
        })
      return result_unlocked
    },
    async checkMetaMask(ABI) {
      if (!this.isLogin) {
        this.notificationInfo("Metamask Wallet Login")
        this.ABI = ABI
        this.W3 = await this.$store.dispatch("wallet/metamaskintegration")
        const getters = this.$store.getters
        if (this.W3) {
          this.networkName = await this.W3.eth.net.getNetworkType()
          this.$store.dispatch("wallet/storeContract", this.contractAddressInfer())
          const contract = getters["wallet/addressContract"]
          this.contractInstance = await new this.W3.eth.Contract(ABI, contract)
          const res = await this.W3.eth.getAccounts()
          const balance_contract = await this.W3.eth.getBalance(contract)
          await this.$store.dispatch("wallet/getContractBalance", balance_contract)
          /* this.basicOptions = {
             gas : 300000,
             from : res[0],
             gasPrice : 0,
             value : this.W3.utils.toWei ("0.1", "ether")
           }; */
          /*  this.txObject = {
              nonce : this.W3.utils.toHex (300000),
              to : res[0],
              value : this.W3.utils.toHex (this.W3.utils.toWei ("0.1", "ether")),
              gasLimit : this.W3.utils.toHex (21000),
              gasPrice : this.W3.utils.toHex (this.W3.utils.toWei ("10", "gwei"))
            }; */
          for (let j = 0; j < res.length; j++) {
            if (j === 0) {
              const myAddress = res[j]
              const balance = await this.W3.eth.getBalance(myAddress) // Will give value in.
              this.$store.commit("wallet/USER_ACCOUNT_INIT", res[j])
              this.$store.commit("wallet/ETH_BAL", balance)
              this.$nextTick(() => {
                this.$emit("login_mask_complete")
              })
              // console.log ("started here  - ", balance)
              this.notificationSuccess("You login with metamask in success.")
            }
          }
        }
      }
    },
    /**
     *     ownable contract
     *     started in here
     */
    async checkFee() {
      try {
        const founder = await this.InvokeGetFunc("owner")
        await this.$store.dispatch("wallet/basicInfo", {
          founder
        })
        await this.getInfoBasicContract()
        this.$store.dispatch("wallet/syncdata", true)
        // this.notificationSuccess ("synced data");
        // console.log ("get info from basic contract");
      } catch (e) {
        this.$store.dispatch("wallet/syncdata", false)
        this.notificationError("offline")
      }
    },
    async masonic_check_only() {
      try {
        const answer = await this.InvokeGetFunc("isOwner")
        this.$store.dispatch("wallet/basicInfoIsFounder", answer)
        this.$store.dispatch("wallet/syncdata")
        await this.getInfoBasicContract()
        this.$store.dispatch("wallet/syncdata", true)
        // this.notificationSuccess ("synced data");
        // console.log ("get info from basic contract");
      } catch (e) {
        this.$store.dispatch("wallet/syncdata", false)
        this.notificationError("offline")
      }
    },
    ownerOnlyAddVip(address) {
      if (!this.isAddress(address)) {
        this.notificationError("This address is invalid")
        return
      }
      if (this.process_f3) {
        this.notificationError("Address append is in progress.")
        return
      }
      this.process_f3 = true
      try {
        const event = this.InvokeWriteFunc("addToVIPList", [[address]])
        event.on("receipt", (receipt) => {
          this.process_f3 = false
          this.notificationSuccess("hash confirmed append address", receipt.transactionHash)
        })
        event.on("error", (e) => {
          this.process_f3 = false
          this.notificationError(e)
        })
      } catch (e) {
        this.notificationError(e)
      }
    },
    async ownerOnlySetCommonFee(amount) {
      if (amount < 0 || this.process_f2) {
        return
      }
      this.process_f2 = true
      try {
        const event = this.InvokeWriteFunc("setTxFee", [this.toWei(amount)])
        event.on("receipt", (receipt) => {
          this.process_f2 = false
          this.notificationSuccess(this.$t("n_hashcfm"), receipt.transactionHash)
        })
        event.on("error", (e) => {
          this.process_f2 = false
          this.notificationError(e)
        })
      } catch (e) {
        this.notificationError(e)
      }
      // send common fee
    },
    async ownerOnlySetVIPFee(amount) {
      if (amount < 0 || this.process_f1) {
        return
      }
      this.process_f1 = true
      try {
        const event = this.InvokeWriteFunc("setVIPFee", [this.toWei(amount)])
        event.on("receipt", (receipt) => {
          this.process_f1 = false
          this.notificationSuccess("hash confirmed vip fee", receipt.transactionHash)
        })
        event.on("error", (e) => {
          this.process_f1 = false
          this.notificationError(e)
        })
      } catch (e) {
        this.notificationError(e)
      }
    },
    joinVip(e) {
      e.preventDefault()
      this.checkFee()
      const event = this.InvokeFunctionEtherCallSend(this.vip_fee, "registerVIP")
      event.on("receipt", (receipt) => {
        this.$emit("register_vip_hash", receipt.transactionHash)
      })
    },
    getReferText() {
      // return "Please enter the code " + this.myinvitationcode + " to join the investment game.";
      return this.myinvitationcode
    },
    copyInviteCode(e) {
      e.preventDefault()
      const that = this
      this.$copyText(this.getReferText()).then(function (e) {
        // alert ('Copied')
        // console.log (e)
        that.notificationSuccess(that.$t("n_copy"))
      }, function (e) {
        that.notificationError(e)
        // alert ('Can not copy')
        // console.log (e)
      })
    }
  }
}
