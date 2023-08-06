import { version, Contract } from "tronweb";
import BaseContract from "./base/base";
export class TRC773 extends BaseContract {
    constructor(tron) {
        super();
        this.__debug = true;
        this.tronweb = null;
        this.based_version = version;
        this.tronweb = tron;
    }
    static Instance() {
        if (window && window.hasOwnProperty("___contract__TRC773__")) {
            const obj = window.___contract__TRC773__;
            if (obj instanceof TRC773) {
                return (obj);
            }
            else {
                return (obj);
            }
        }
        else {
            return false;
        }
    }
    async init(contract_address) {
        this.contract = await new Contract(this.tronweb, TRC773.ABI(), contract_address);
        this.contract_address_t = contract_address;
        if (window && !window.hasOwnProperty("___contract__TRC773__")) {
            window.___contract__TRC773__ = this;
        }
    }
    setDebug(bool) {
        this.__debug = bool;
    }
    isVersionCompatible() {
        return this.based_version === this.tronweb.version;
    }
    async SERVICE_FEE() {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0
        };
        const val = await this.contract.SERVICE_FEE()
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 SERVICE_FEE");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async __callback(_myid, _result) {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0
        };
        const val = await this.contract.__callback(_myid, _result)
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 __callback");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async addCroupier(account) {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0
        };
        const val = await this.contract.addCroupier(account)
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 addCroupier");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async addWhitelistAdmin(account) {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0
        };
        const val = await this.contract.addWhitelistAdmin(account)
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 addWhitelistAdmin");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async allTickets(index_0) {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0
        };
        const val = await this.contract.allTickets(index_0)
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 allTickets");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async bankAddress() {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0
        };
        const val = await this.contract.bankAddress()
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 bankAddress");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async buyTicket(combo, referrer, trx) {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: trx
        };
        const val = await this.contract.buyTicket(combo, referrer)
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 buyTicket");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async changeSettings(hour, gMin, tktPrice) {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0
        };
        const val = await this.contract.changeSettings(hour, gMin, tktPrice)
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 changeSettings");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async checkhash() {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0
        };
        const val = await this.contract.checkhash()
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 checkhash");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async compareStr(src, src_compared) {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0
        };
        const val = await this.contract.compareStr(src, src_compared)
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 compareStr");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async contractInvalidate() {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0
        };
        const val = await this.contract.contractInvalidate()
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 contractInvalidate");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async depositFundsTrx(trx) {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: trx
        };
        const val = await this.contract.depositFundsTrx()
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 depositFundsTrx");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async drawWin(hash) {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0
        };
        const val = await this.contract.drawWin(hash)
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 drawWin");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async getHistory() {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0
        };
        const val = await this.contract.getHistory()
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 getHistory");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async getPlayerUnclaimedTickets() {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0
        };
        const val = await this.contract.getPlayerUnclaimedTickets()
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 getPlayerUnclaimedTickets");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async hasRequestedGame(index_0) {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0
        };
        const val = await this.contract.hasRequestedGame(index_0)
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 hasRequestedGame");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async hashcall() {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0
        };
        const val = await this.contract.hashcall()
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 hashcall");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async isCroupier(account) {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0
        };
        const val = await this.contract.isCroupier(account)
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 isCroupier");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async isLocked() {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0
        };
        const val = await this.contract.isLocked()
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 isLocked");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async isOwner() {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0
        };
        const val = await this.contract.isOwner()
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 isOwner");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async isWhitelistAdmin(account) {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0
        };
        const val = await this.contract.isWhitelistAdmin(account)
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 isWhitelistAdmin");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async katana() {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0
        };
        const val = await this.contract.katana()
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 katana");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async lock() {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0
        };
        const val = await this.contract.lock()
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 lock");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async owner() {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0
        };
        const val = await this.contract.owner()
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 owner");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async pendingQueries(index_0) {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0
        };
        const val = await this.contract.pendingQueries(index_0)
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 pendingQueries");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async playerList() {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0
        };
        const val = await this.contract.playerList()
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 playerList");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async playerTotal(_address) {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0
        };
        const val = await this.contract.playerTotal(_address)
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 playerTotal");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async registeredFunds(index_0) {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0
        };
        const val = await this.contract.registeredFunds(index_0)
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 registeredFunds");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async removeCroupier(account) {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0
        };
        const val = await this.contract.removeCroupier(account)
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 removeCroupier");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async removeWhitelistAdmin(account) {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0
        };
        const val = await this.contract.removeWhitelistAdmin(account)
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 removeWhitelistAdmin");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async renounceOwnership() {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0
        };
        const val = await this.contract.renounceOwnership()
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 renounceOwnership");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async shenzhen() {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0
        };
        const val = await this.contract.shenzhen()
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 shenzhen");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async stringToBytes32(source) {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0
        };
        const val = await this.contract.stringToBytes32(source)
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 stringToBytes32");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async ticketKeys(index_0, index_1) {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0
        };
        const val = await this.contract.ticketKeys(index_0, index_1)
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 ticketKeys");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async transferOwnership(newOwner) {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0
        };
        const val = await this.contract.transferOwnership(newOwner)
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 transferOwnership");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async unlock() {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0
        };
        const val = await this.contract.unlock()
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 unlock");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async withdrawFundsTrx() {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0
        };
        const val = await this.contract.withdrawFundsTrx()
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 withdrawFundsTrx");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async zjLimits(wtrx, sinktrx) {
        const callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0
        };
        const val = await this.contract.zjLimits(wtrx, sinktrx)
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 zjLimits");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async eventQ(event_name, page, since = 0) {
        const data = await this.tronweb && this.contract && this.tronweb.getEventResult(this.contract_address_t, since, event_name, 0, 20, page);
        return data;
    }
    async startEventListeners() {
        await this.contract && this.contract.BetsLocked().watch((err, event_payload) => {
            if (err) {
                return console.error("Failed to bind event listener:", err);
            }
            if (event_payload) {
                const { result, block, transaction, name, contract } = event_payload;
                if (this.__debug) {
                    console.group("New event received");
                    console.log("- Contract Address:", contract);
                    console.log("- Event Name:", name);
                    console.log("- Transaction:", transaction);
                    console.log("- Block number:", block);
                    console.log("- Result:", result, "\n");
                    console.groupEnd();
                }
                this.emit("event_BetsLocked", event_payload);
            }
        });
        await this.contract && this.contract.CheckResult().watch((err, event_payload) => {
            if (err) {
                return console.error("Failed to bind event listener:", err);
            }
            if (event_payload) {
                const { result, block, transaction, name, contract } = event_payload;
                if (this.__debug) {
                    console.group("New event received");
                    console.log("- Contract Address:", contract);
                    console.log("- Event Name:", name);
                    console.log("- Transaction:", transaction);
                    console.log("- Block number:", block);
                    console.log("- Result:", result, "\n");
                    console.groupEnd();
                }
                this.emit("event_CheckResult", event_payload);
            }
        });
        await this.contract && this.contract.Commit().watch((err, event_payload) => {
            if (err) {
                return console.error("Failed to bind event listener:", err);
            }
            if (event_payload) {
                const { result, block, transaction, name, contract } = event_payload;
                if (this.__debug) {
                    console.group("New event received");
                    console.log("- Contract Address:", contract);
                    console.log("- Event Name:", name);
                    console.log("- Transaction:", transaction);
                    console.log("- Block number:", block);
                    console.log("- Result:", result, "\n");
                    console.groupEnd();
                }
                this.emit("event_Commit", event_payload);
            }
        });
        await this.contract && this.contract.DrawDismiss().watch((err, event_payload) => {
            if (err) {
                return console.error("Failed to bind event listener:", err);
            }
            if (event_payload) {
                const { result, block, transaction, name, contract } = event_payload;
                if (this.__debug) {
                    console.group("New event received");
                    console.log("- Contract Address:", contract);
                    console.log("- Event Name:", name);
                    console.log("- Transaction:", transaction);
                    console.log("- Block number:", block);
                    console.log("- Result:", result, "\n");
                    console.groupEnd();
                }
                this.emit("event_DrawDismiss", event_payload);
            }
        });
        await this.contract && this.contract.FailedPayment().watch((err, event_payload) => {
            if (err) {
                return console.error("Failed to bind event listener:", err);
            }
            if (event_payload) {
                const { result, block, transaction, name, contract } = event_payload;
                if (this.__debug) {
                    console.group("New event received");
                    console.log("- Contract Address:", contract);
                    console.log("- Event Name:", name);
                    console.log("- Transaction:", transaction);
                    console.log("- Block number:", block);
                    console.log("- Result:", result, "\n");
                    console.groupEnd();
                }
                this.emit("event_FailedPayment", event_payload);
            }
        });
        await this.contract && this.contract.OwnershipTransferred().watch((err, event_payload) => {
            if (err) {
                return console.error("Failed to bind event listener:", err);
            }
            if (event_payload) {
                const { result, block, transaction, name, contract } = event_payload;
                if (this.__debug) {
                    console.group("New event received");
                    console.log("- Contract Address:", contract);
                    console.log("- Event Name:", name);
                    console.log("- Transaction:", transaction);
                    console.log("- Block number:", block);
                    console.log("- Result:", result, "\n");
                    console.groupEnd();
                }
                this.emit("event_OwnershipTransferred", event_payload);
            }
        });
        await this.contract && this.contract.Payment().watch((err, event_payload) => {
            if (err) {
                return console.error("Failed to bind event listener:", err);
            }
            if (event_payload) {
                const { result, block, transaction, name, contract } = event_payload;
                if (this.__debug) {
                    console.group("New event received");
                    console.log("- Contract Address:", contract);
                    console.log("- Event Name:", name);
                    console.log("- Transaction:", transaction);
                    console.log("- Block number:", block);
                    console.log("- Result:", result, "\n");
                    console.groupEnd();
                }
                this.emit("event_Payment", event_payload);
            }
        });
        await this.contract && this.contract.PurchaseTicket().watch((err, event_payload) => {
            if (err) {
                return console.error("Failed to bind event listener:", err);
            }
            if (event_payload) {
                const { result, block, transaction, name, contract } = event_payload;
                if (this.__debug) {
                    console.group("New event received");
                    console.log("- Contract Address:", contract);
                    console.log("- Event Name:", name);
                    console.log("- Transaction:", transaction);
                    console.log("- Block number:", block);
                    console.log("- Result:", result, "\n");
                    console.groupEnd();
                }
                this.emit("event_PurchaseTicket", event_payload);
            }
        });
        await this.contract && this.contract.ReferralPayment().watch((err, event_payload) => {
            if (err) {
                return console.error("Failed to bind event listener:", err);
            }
            if (event_payload) {
                const { result, block, transaction, name, contract } = event_payload;
                if (this.__debug) {
                    console.group("New event received");
                    console.log("- Contract Address:", contract);
                    console.log("- Event Name:", name);
                    console.log("- Transaction:", transaction);
                    console.log("- Block number:", block);
                    console.log("- Result:", result, "\n");
                    console.groupEnd();
                }
                this.emit("event_ReferralPayment", event_payload);
            }
        });
        await this.contract && this.contract.WinningNumbers().watch((err, event_payload) => {
            if (err) {
                return console.error("Failed to bind event listener:", err);
            }
            if (event_payload) {
                const { result, block, transaction, name, contract } = event_payload;
                if (this.__debug) {
                    console.group("New event received");
                    console.log("- Contract Address:", contract);
                    console.log("- Event Name:", name);
                    console.log("- Transaction:", transaction);
                    console.log("- Block number:", block);
                    console.log("- Result:", result, "\n");
                    console.groupEnd();
                }
                this.emit("event_WinningNumbers", event_payload);
            }
        });
        await this.contract && this.contract.traillock().watch((err, event_payload) => {
            if (err) {
                return console.error("Failed to bind event listener:", err);
            }
            if (event_payload) {
                const { result, block, transaction, name, contract } = event_payload;
                if (this.__debug) {
                    console.group("New event received");
                    console.log("- Contract Address:", contract);
                    console.log("- Event Name:", name);
                    console.log("- Transaction:", transaction);
                    console.log("- Block number:", block);
                    console.log("- Result:", result, "\n");
                    console.groupEnd();
                }
                this.emit("event_traillock", event_payload);
            }
        });
    }
    static ABI() {
        const abi = [
            {
                inputs: [],
                outputs: [],
                payable: false,
                stateMutability: "nonpayable",
                type: "constructor"
            },
            {
                anonymous: false,
                inputs: [
                    {
                        name: "locker",
                        type: "address",
                        indexed: true
                    }
                ],
                name: "BetsLocked",
                outputs: [],
                type: "event"
            },
            {
                anonymous: false,
                inputs: [
                    {
                        name: "checker",
                        type: "address",
                        indexed: true
                    },
                    {
                        name: "found",
                        type: "uint8",
                        indexed: false
                    },
                    {
                        name: "size",
                        type: "uint256",
                        indexed: false
                    },
                    {
                        name: "amount",
                        type: "uint256",
                        indexed: false
                    }
                ],
                name: "CheckResult",
                outputs: [],
                type: "event"
            },
            {
                anonymous: false,
                inputs: [
                    {
                        name: "commit",
                        type: "address",
                        indexed: false
                    }
                ],
                name: "Commit",
                outputs: [],
                type: "event"
            },
            {
                anonymous: false,
                inputs: [
                    {
                        name: "checker",
                        type: "address",
                        indexed: true
                    },
                    {
                        name: "round",
                        type: "uint256",
                        indexed: false
                    }
                ],
                name: "DrawDismiss",
                outputs: [],
                type: "event"
            },
            {
                anonymous: false,
                inputs: [
                    {
                        name: "beneficiary",
                        type: "address",
                        indexed: true
                    },
                    {
                        name: "amount",
                        type: "uint256",
                        indexed: false
                    }
                ],
                name: "FailedPayment",
                outputs: [],
                type: "event"
            },
            {
                anonymous: false,
                inputs: [
                    {
                        name: "previousOwner",
                        type: "address",
                        indexed: true
                    },
                    {
                        name: "newOwner",
                        type: "address",
                        indexed: true
                    }
                ],
                name: "OwnershipTransferred",
                outputs: [],
                type: "event"
            },
            {
                anonymous: false,
                inputs: [
                    {
                        name: "beneficiary",
                        type: "address",
                        indexed: true
                    },
                    {
                        name: "amount",
                        type: "uint256",
                        indexed: false
                    }
                ],
                name: "Payment",
                outputs: [],
                type: "event"
            },
            {
                anonymous: false,
                inputs: [
                    {
                        name: "buyer",
                        type: "address",
                        indexed: true
                    },
                    {
                        name: "amount",
                        type: "uint256",
                        indexed: false
                    }
                ],
                name: "PurchaseTicket",
                outputs: [],
                type: "event"
            },
            {
                anonymous: false,
                inputs: [
                    {
                        name: "beneficiary",
                        type: "address",
                        indexed: true
                    },
                    {
                        name: "amount",
                        type: "uint256",
                        indexed: false
                    }
                ],
                name: "ReferralPayment",
                outputs: [],
                type: "event"
            },
            {
                anonymous: false,
                inputs: [
                    {
                        name: "openNum",
                        type: "uint8[10]",
                        indexed: false
                    }
                ],
                name: "WinningNumbers",
                outputs: [],
                type: "event"
            },
            {
                anonymous: false,
                inputs: [
                    {
                        name: "value",
                        type: "uint8",
                        indexed: false
                    }
                ],
                name: "traillock",
                outputs: [],
                type: "event"
            },
            {
                constant: true,
                inputs: [],
                name: "SERVICE_FEE",
                outputs: [
                    {
                        name: "",
                        type: "uint256"
                    }
                ],
                payable: false,
                stateMutability: "view",
                type: "function"
            },
            {
                constant: false,
                inputs: [
                    {
                        name: "_myid",
                        type: "bytes32"
                    },
                    {
                        name: "_result",
                        type: "string"
                    }
                ],
                name: "__callback",
                outputs: [],
                payable: false,
                stateMutability: "nonpayable",
                type: "function"
            },
            {
                constant: false,
                inputs: [
                    {
                        name: "account",
                        type: "address"
                    }
                ],
                name: "addCroupier",
                outputs: [],
                payable: false,
                stateMutability: "nonpayable",
                type: "function"
            },
            {
                constant: false,
                inputs: [
                    {
                        name: "account",
                        type: "address"
                    }
                ],
                name: "addWhitelistAdmin",
                outputs: [],
                payable: false,
                stateMutability: "nonpayable",
                type: "function"
            },
            {
                constant: true,
                inputs: [
                    {
                        name: "index_0",
                        type: "uint256"
                    }
                ],
                name: "allTickets",
                outputs: [
                    {
                        name: "playerAddress",
                        type: "address"
                    },
                    {
                        name: "price",
                        type: "uint256"
                    },
                    {
                        name: "startRound",
                        type: "uint48"
                    },
                    {
                        name: "inRound",
                        type: "uint48"
                    }
                ],
                payable: false,
                stateMutability: "view",
                type: "function"
            },
            {
                constant: true,
                inputs: [],
                name: "bankAddress",
                outputs: [
                    {
                        name: "",
                        type: "address"
                    }
                ],
                payable: false,
                stateMutability: "view",
                type: "function"
            },
            {
                constant: false,
                inputs: [
                    {
                        name: "combo",
                        type: "uint8[]"
                    },
                    {
                        name: "referrer",
                        type: "address"
                    }
                ],
                name: "buyTicket",
                outputs: [],
                payable: true,
                stateMutability: "payable",
                type: "function"
            },
            {
                constant: false,
                inputs: [
                    {
                        name: "hour",
                        type: "uint256"
                    },
                    {
                        name: "gMin",
                        type: "uint256"
                    },
                    {
                        name: "tktPrice",
                        type: "uint256"
                    }
                ],
                name: "changeSettings",
                outputs: [],
                payable: false,
                stateMutability: "nonpayable",
                type: "function"
            },
            {
                constant: true,
                inputs: [],
                name: "checkhash",
                outputs: [
                    {
                        name: "hash",
                        type: "bytes32[3]"
                    }
                ],
                payable: false,
                stateMutability: "view",
                type: "function"
            },
            {
                constant: true,
                inputs: [
                    {
                        name: "src",
                        type: "string"
                    },
                    {
                        name: "src_compared",
                        type: "string"
                    }
                ],
                name: "compareStr",
                outputs: [
                    {
                        name: "",
                        type: "bool"
                    }
                ],
                payable: false,
                stateMutability: "pure",
                type: "function"
            },
            {
                constant: false,
                inputs: [],
                name: "contractInvalidate",
                outputs: [],
                payable: false,
                stateMutability: "nonpayable",
                type: "function"
            },
            {
                constant: false,
                inputs: [],
                name: "depositFundsTrx",
                outputs: [],
                payable: true,
                stateMutability: "payable",
                type: "function"
            },
            {
                constant: false,
                inputs: [
                    {
                        name: "hash",
                        type: "bytes32"
                    }
                ],
                name: "drawWin",
                outputs: [
                    {
                        name: "",
                        type: "bool"
                    }
                ],
                payable: false,
                stateMutability: "nonpayable",
                type: "function"
            },
            {
                constant: true,
                inputs: [],
                name: "getHistory",
                outputs: [
                    {
                        name: "",
                        type: "uint256[10]"
                    }
                ],
                payable: false,
                stateMutability: "view",
                type: "function"
            },
            {
                constant: true,
                inputs: [],
                name: "getPlayerUnclaimedTickets",
                outputs: [
                    {
                        name: "",
                        type: "uint256[]"
                    },
                    {
                        name: "",
                        type: "uint48[]"
                    },
                    {
                        name: "",
                        type: "uint48[]"
                    },
                    {
                        name: "",
                        type: "uint256[]"
                    }
                ],
                payable: false,
                stateMutability: "view",
                type: "function"
            },
            {
                constant: true,
                inputs: [
                    {
                        name: "index_0",
                        type: "address"
                    }
                ],
                name: "hasRequestedGame",
                outputs: [
                    {
                        name: "",
                        type: "bool"
                    }
                ],
                payable: false,
                stateMutability: "view",
                type: "function"
            },
            {
                constant: false,
                inputs: [],
                name: "hashcall",
                outputs: [],
                payable: false,
                stateMutability: "nonpayable",
                type: "function"
            },
            {
                constant: true,
                inputs: [
                    {
                        name: "account",
                        type: "address"
                    }
                ],
                name: "isCroupier",
                outputs: [
                    {
                        name: "",
                        type: "bool"
                    }
                ],
                payable: false,
                stateMutability: "view",
                type: "function"
            },
            {
                constant: true,
                inputs: [],
                name: "isLocked",
                outputs: [
                    {
                        name: "",
                        type: "bool"
                    }
                ],
                payable: false,
                stateMutability: "view",
                type: "function"
            },
            {
                constant: true,
                inputs: [],
                name: "isOwner",
                outputs: [
                    {
                        name: "",
                        type: "bool"
                    }
                ],
                payable: false,
                stateMutability: "view",
                type: "function"
            },
            {
                constant: true,
                inputs: [
                    {
                        name: "account",
                        type: "address"
                    }
                ],
                name: "isWhitelistAdmin",
                outputs: [
                    {
                        name: "",
                        type: "bool"
                    }
                ],
                payable: false,
                stateMutability: "view",
                type: "function"
            },
            {
                constant: false,
                inputs: [],
                name: "katana",
                outputs: [],
                payable: false,
                stateMutability: "nonpayable",
                type: "function"
            },
            {
                constant: false,
                inputs: [],
                name: "lock",
                outputs: [],
                payable: false,
                stateMutability: "nonpayable",
                type: "function"
            },
            {
                constant: true,
                inputs: [],
                name: "owner",
                outputs: [
                    {
                        name: "",
                        type: "address"
                    }
                ],
                payable: false,
                stateMutability: "view",
                type: "function"
            },
            {
                constant: true,
                inputs: [
                    {
                        name: "index_0",
                        type: "bytes32"
                    }
                ],
                name: "pendingQueries",
                outputs: [
                    {
                        name: "",
                        type: "bool"
                    }
                ],
                payable: false,
                stateMutability: "view",
                type: "function"
            },
            {
                constant: true,
                inputs: [],
                name: "playerList",
                outputs: [
                    {
                        name: "_addresses",
                        type: "address[]"
                    },
                    {
                        name: "_values",
                        type: "uint256[]"
                    }
                ],
                payable: false,
                stateMutability: "view",
                type: "function"
            },
            {
                constant: true,
                inputs: [
                    {
                        name: "_address",
                        type: "address"
                    }
                ],
                name: "playerTotal",
                outputs: [
                    {
                        name: "",
                        type: "uint256"
                    }
                ],
                payable: false,
                stateMutability: "view",
                type: "function"
            },
            {
                constant: true,
                inputs: [
                    {
                        name: "index_0",
                        type: "address"
                    }
                ],
                name: "registeredFunds",
                outputs: [
                    {
                        name: "",
                        type: "uint256"
                    }
                ],
                payable: false,
                stateMutability: "view",
                type: "function"
            },
            {
                constant: false,
                inputs: [
                    {
                        name: "account",
                        type: "address"
                    }
                ],
                name: "removeCroupier",
                outputs: [],
                payable: false,
                stateMutability: "nonpayable",
                type: "function"
            },
            {
                constant: false,
                inputs: [
                    {
                        name: "account",
                        type: "address"
                    }
                ],
                name: "removeWhitelistAdmin",
                outputs: [],
                payable: false,
                stateMutability: "nonpayable",
                type: "function"
            },
            {
                constant: false,
                inputs: [],
                name: "renounceOwnership",
                outputs: [],
                payable: false,
                stateMutability: "nonpayable",
                type: "function"
            },
            {
                constant: true,
                inputs: [],
                name: "shenzhen",
                outputs: [
                    {
                        name: "lottoInfo",
                        type: "uint256[13]"
                    },
                    {
                        name: "early_birds",
                        type: "address[]"
                    },
                    {
                        name: "flags",
                        type: "bool[4]"
                    }
                ],
                payable: false,
                stateMutability: "view",
                type: "function"
            },
            {
                constant: true,
                inputs: [
                    {
                        name: "source",
                        type: "string"
                    }
                ],
                name: "stringToBytes32",
                outputs: [
                    {
                        name: "result",
                        type: "bytes32"
                    }
                ],
                payable: false,
                stateMutability: "pure",
                type: "function"
            },
            {
                constant: true,
                inputs: [
                    {
                        name: "index_0",
                        type: "address"
                    },
                    {
                        name: "index_1",
                        type: "uint256"
                    }
                ],
                name: "ticketKeys",
                outputs: [
                    {
                        name: "",
                        type: "uint256"
                    }
                ],
                payable: false,
                stateMutability: "view",
                type: "function"
            },
            {
                constant: false,
                inputs: [
                    {
                        name: "newOwner",
                        type: "address"
                    }
                ],
                name: "transferOwnership",
                outputs: [],
                payable: false,
                stateMutability: "nonpayable",
                type: "function"
            },
            {
                constant: false,
                inputs: [],
                name: "unlock",
                outputs: [],
                payable: false,
                stateMutability: "nonpayable",
                type: "function"
            },
            {
                constant: false,
                inputs: [],
                name: "withdrawFundsTrx",
                outputs: [],
                payable: false,
                stateMutability: "nonpayable",
                type: "function"
            },
            {
                constant: false,
                inputs: [
                    {
                        name: "wtrx",
                        type: "uint256"
                    },
                    {
                        name: "sinktrx",
                        type: "uint256"
                    }
                ],
                name: "zjLimits",
                outputs: [],
                payable: false,
                stateMutability: "nonpayable",
                type: "function"
            }
        ];
        return abi;
    }
}
TRC773.deployedBytecode = "60806040526003805461ff01600160b01b03191675a5576e55542477ce999f2d3a8c242697b0fcf41600001790556004805473a5576e55542477ce999f2d3a8c242697b0fcf4166001600160a01b0319909116179055600060055562000077620f424061271062000152602090811b6200398417901c565b600655620000996103e8620f42406200015260201b620039841790919060201c565b6007556008805460ff19908116909155600e805490911690556025805461ffff19169055348015620000ca57600080fd5b506000620000e06001600160e01b036200017c16565b600080546001600160a01b0319166001600160a01b0383169081178255604051929350917f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e0908290a3506003805461ff0019166101001790556200014c6001600160e01b036200018016565b620001bd565b60008282028315806200016e5750828482816200016b57fe5b04145b6200017557fe5b9392505050565b3390565b6000601d819055601655426018556015805465ffffffffffff19166127101790556305f5e100601c556201a5e0601955610320601a556078601b55565b614ea080620001cd6000396000f3fe6080604052600436106102255760003560e01c80638f32d59b11610123578063bc7e9c5c116100ab578063d93eda0f1161006f578063d93eda0f14610ba3578063de724c4b14610bdc578063e3ede05b14610c7e578063f2fde38b14610c93578063f83d08ba14610cc657610225565b8063bc7e9c5c14610a3c578063c599741914610a51578063cfb5192814610a66578063d0a753af14610b17578063d2e97d8614610b7957610225565b8063a626c089116100f2578063a626c0891461093d578063a69df4b514610973578063aa15efc814610988578063b3a5cec6146109d6578063bb5f747b14610a0957610225565b80638f32d59b146108ad5780639c40944d146108c2578063a3ec6b60146108f5578063a4e2d6341461092857610225565b806361ff6e64116101b15780637826d064116101755780637826d064146106d55780637f02d9051461070557806387c5d5cc1461073857806389a2cdcb1461086e5780638da5cb5b1461089857610225565b806361ff6e64146106215780636897e97414610629578063715018a61461065c5780637362d9c8146106715780637822ed49146106a457610225565b806330f95a56116101f857806330f95a561461046f57806344268655146104b4578063506592f5146104e757806350c86de51461055e5780635fc5d46d1461057357610225565b806301ef264d1461022a578063052e74d1146103625780630c64589d146103a057806327dc297e146103b7575b600080fd5b34801561023657600080fd5b5061023f610cdb565b6040518080602001806020018060200180602001858103855289818151815260200191508051906020019060200280838360005b8381101561028b578181015183820152602001610273565b50505050905001858103845288818151815260200191508051906020019060200280838360005b838110156102ca5781810151838201526020016102b2565b50505050905001858103835287818151815260200191508051906020019060200280838360005b838110156103095781810151838201526020016102f1565b50505050905001858103825286818151815260200191508051906020019060200280838360005b83811015610348578181015183820152602001610330565b505050509050019850505050505050505060405180910390f35b34801561036e57600080fd5b5061038c6004803603602081101561038557600080fd5b5035610fec565b604080519115158252519081900360200190f35b3480156103ac57600080fd5b506103b56113db565b005b3480156103c357600080fd5b506103b5600480360360408110156103da57600080fd5b81359190810190604081016020820135600160201b8111156103fb57600080fd5b82018360208201111561040d57600080fd5b803590602001918460018302840111600160201b8311171561042e57600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600092019190915250929550611459945050505050565b34801561047b57600080fd5b506104a26004803603602081101561049257600080fd5b50356001600160a01b031661162a565b60408051918252519081900360200190f35b3480156104c057600080fd5b506103b5600480360360208110156104d757600080fd5b50356001600160a01b03166116cc565b6103b5600480360360408110156104fd57600080fd5b810190602081018135600160201b81111561051757600080fd5b82018360208201111561052957600080fd5b803590602001918460208302840111600160201b8311171561054a57600080fd5b9193509150356001600160a01b0316611731565b34801561056a57600080fd5b506104a261195a565b34801561057f57600080fd5b5061058861195f565b604051808060200180602001838103835285818151815260200191508051906020019060200280838360005b838110156105cc5781810151838201526020016105b4565b50505050905001838103825284818151815260200191508051906020019060200280838360005b8381101561060b5781810151838201526020016105f3565b5050505090500194505050505060405180910390f35b6103b5611ae3565b34801561063557600080fd5b506103b56004803603602081101561064c57600080fd5b50356001600160a01b0316611bbd565b34801561066857600080fd5b506103b5611c15565b34801561067d57600080fd5b506103b56004803603602081101561069457600080fd5b50356001600160a01b0316611ca6565b3480156106b057600080fd5b506106b9611cfe565b604080516001600160a01b039092168252519081900360200190f35b3480156106e157600080fd5b506103b5600480360360408110156106f857600080fd5b5080359060200135611d12565b34801561071157600080fd5b5061038c6004803603602081101561072857600080fd5b50356001600160a01b0316611e8e565b34801561074457600080fd5b5061038c6004803603604081101561075b57600080fd5b810190602081018135600160201b81111561077557600080fd5b82018360208201111561078757600080fd5b803590602001918460018302840111600160201b831117156107a857600080fd5b91908080601f0160208091040260200160405190810160405280939291908181526020018383808284376000920191909152509295949360208101935035915050600160201b8111156107fa57600080fd5b82018360208201111561080c57600080fd5b803590602001918460018302840111600160201b8311171561082d57600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600092019190915250929550611ea3945050505050565b34801561087a57600080fd5b5061038c6004803603602081101561089157600080fd5b5035611f99565b3480156108a457600080fd5b506106b9611fae565b3480156108b957600080fd5b5061038c611fbe565b3480156108ce57600080fd5b506103b5600480360360208110156108e557600080fd5b50356001600160a01b0316611fe2565b34801561090157600080fd5b5061038c6004803603602081101561091857600080fd5b50356001600160a01b0316612047565b34801561093457600080fd5b5061038c612068565b34801561094957600080fd5b506103b56004803603606081101561096057600080fd5b5080359060208101359060400135612074565b34801561097f57600080fd5b506103b56120f1565b34801561099457600080fd5b5061099d61214f565b604051808261014080838360005b838110156109c35781810151838201526020016109ab565b5050505090500191505060405180910390f35b3480156109e257600080fd5b506104a2600480360360208110156109f957600080fd5b50356001600160a01b031661220c565b348015610a1557600080fd5b5061038c60048036036020811015610a2c57600080fd5b50356001600160a01b031661221e565b348015610a4857600080fd5b506103b5612231565b348015610a5d57600080fd5b506103b56123c9565b348015610a7257600080fd5b506104a260048036036020811015610a8957600080fd5b810190602081018135600160201b811115610aa357600080fd5b820183602082011115610ab557600080fd5b803590602001918460018302840111600160201b83111715610ad657600080fd5b91908080601f0160208091040260200160405190810160405280939291908181526020018383808284376000920191909152509295506124d4945050505050565b348015610b2357600080fd5b50610b4160048036036020811015610b3a57600080fd5b50356124f2565b604080516001600160a01b039095168552602085019390935265ffffffffffff91821684840152166060830152519081900360800190f35b348015610b8557600080fd5b50610b8e612530565b604051815181528082606080838360206109ab565b348015610baf57600080fd5b506104a260048036036040811015610bc657600080fd5b506001600160a01b0381351690602001356125a8565b348015610be857600080fd5b50610bf16125d6565b60405180846101a080838360005b83811015610c17578181015183820152602001610bff565b50505092019150506020810183608080838360005b83811015610c44578181015183820152602001610c2c565b505050509190910183810383528551815285516020918201925081870191028083836000831561060b5781810151838201526020016105f3565b348015610c8a57600080fd5b506103b56126a5565b348015610c9f57600080fd5b506103b560048036036020811015610cb657600080fd5b50356001600160a01b0316612705565b348015610cd257600080fd5b506103b5612755565b606080606080600060146000610cef6127b1565b6001600160a01b03166001600160a01b03168152602001908152602001600020805490509050606081604051908082528060200260200182016040528015610d41578160200160208202803883390190505b509050606082604051908082528060200260200182016040528015610d70578160200160208202803883390190505b509050606083604051908082528060200260200182016040528015610d9f578160200160208202803883390190505b509050606084604051908082528060200260200182016040528015610dce578160200160208202803883390190505b50905060005b85811015610fdc5760146000610de86127b1565b6001600160a01b03166001600160a01b031681526020019081526020016000208181548110610e1357fe5b9060005260206000200154858281518110610e2a57fe5b6020026020010181815250506012600060146000610e466127b1565b6001600160a01b03166001600160a01b031681526020019081526020016000208381548110610e7157fe5b9060005260206000200154815260200190815260200160002060020160009054906101000a900465ffffffffffff16848281518110610eac57fe5b602002602001019065ffffffffffff16908165ffffffffffff16815250506012600060146000610eda6127b1565b6001600160a01b03166001600160a01b031681526020019081526020016000208381548110610f0557fe5b9060005260206000200154815260200190815260200160002060020160069054906101000a900465ffffffffffff16838281518110610f4057fe5b602002602001019065ffffffffffff16908165ffffffffffff1681525050610fbd6012600060146000610f716127b1565b6001600160a01b03166001600160a01b031681526020019081526020016000208481548110610f9c57fe5b906000526020600020015481526020019081526020016000206003016127b5565b828281518110610fc957fe5b6020908102919091010152600101610dd4565b5092989197509550909350915050565b600354600090610100900460ff16611039576040805162461bcd60e51b815260206004820152601f6024820152600080516020614ca4833981519152604482015290519081900360640190fd5b6003805461ff0019169055600061104e6127b1565b9050803b8015611099576040805162461bcd60e51b8152602060048201526011602482015270736f7272792068756d616e73206f6e6c7960781b604482015290519081900360640190fd5b6110a16127b1565b6001600160a01b0316326001600160a01b0316146110fb576040805162461bcd60e51b8152602060048201526012602482015271736f7272792c2068756d616e73206f6e6c7960701b604482015290519081900360640190fd5b611103612806565b611149576040805162461bcd60e51b81526020600482015260126024820152712a37b79032b0b9363c903a3790323930bb9760711b604482015290519081900360640190fd5b6000611153612812565b9050600061115f612843565b905081801561116c575080155b1561117c576000945050506113c5565b6111846149de565b61119d611198886111936127b1565b6128d6565b6129d0565b4260185590506111ab6129e9565b60155465ffffffffffff16600090815260106020908152604090912082516111dd9360019092019291909101906149fd565b506017546015805465ffffffffffff9081166000908152601060205260408082206005019490945582548083168252848220600301805465ffffffffffff60a01b1916600160301b9092048416600160a01b02919091179055601854835483168252848220600401559154168152204360069091015561125b6127b1565b6015805465ffffffffffff90811660009081526010602052604080822060030180546001600160a01b0319166001600160a01b0396909616959095179094559154168152206112af9060020182600a614a5e565b5060155465ffffffffffff166000908152601060205260409020600701805460ff19168415801591909117909155611342577fa4987dfe08652a7d852b7bf4dcedeab4d39153414e839948d59c9e1f55a4805a816040518082600a60200280838360005b8381101561132b578181015183820152602001611313565b5050505090500191505060405180910390a1611396565b61134a6127b1565b6015546040805165ffffffffffff9092168252516001600160a01b0392909216917f33dc339b9af3901a64dab425610b82eef699967b8a98e3e6b487c3fb142ba3059181900360200190a25b5050601580546001600160601b03198116600165ffffffffffff92831681019092161790915560006017559350505b50506003805461ff001916610100179055919050565b6113eb6113e66127b1565b61221e565b806113f957506113f9611fbe565b6114345760405162461bcd60e51b8152600401808060200182810382526040815260200180614e2c6040913960400191505060405180910390fd5b60058054600090915561144e6114486127b1565b82612ae4565b61145661214d565b50565b611461612b3a565b6001600160a01b0316336001600160a01b03161461147e57600080fd5b6000828152601e602052604090205460ff16151560011461149e57600080fd5b601f548214156114ee576114b1816124d4565b602255601f546000908152601e60205260409020805460ff199081169091556025805460001960ff8281169190910116921691909117905561158b565b60205482141561153f57611501816124d4565b602355602080546000908152601e90915260409020805460ff199081169091556025805460001960ff8281169190910116921691909117905561158b565b60215482141561158b57611552816124d4565b6024556021546000908152601e60205260409020805460ff199081169091556025805460001960ff828116919091011692169190911790555b6000816040516020018082805190602001908083835b602083106115c05780518252601f1990920191602091820191016115a1565b6001836020036101000a03801982511681845116808217855250505050505090500191505060405160208183030381529060405280519060200120905060038160001c8161160a57fe5b06602560016101000a81548160ff021916908360ff160217905550505050565b6001600160a01b03811660009081526013602052604081205460155465ffffffffffff91821691600160301b9091041681118061166d575065ffffffffffff8116155b8061169b575065ffffffffffff81166000908152601160205260409020546001600160a01b03848116911614155b156116aa5760009150506116c7565b65ffffffffffff1660009081526011602052604090206001015490505b919050565b6116d76113e66127b1565b806116e557506116e5611fbe565b6117205760405162461bcd60e51b8152600401808060200182810382526040815260200180614e2c6040913960400191505060405180910390fd5b61145660028263ffffffff612d4816565b600354610100900460ff1661177b576040805162461bcd60e51b815260206004820152601f6024820152600080516020614ca4833981519152604482015290519081900360640190fd5b6003805461ff001916905560006117906127b1565b9050803b80156117db576040805162461bcd60e51b8152602060048201526011602482015270736f7272792068756d616e73206f6e6c7960781b604482015290519081900360640190fd5b6117e36127b1565b6001600160a01b0316326001600160a01b03161461183d576040805162461bcd60e51b8152602060048201526012602482015271736f7272792c2068756d616e73206f6e6c7960701b604482015290519081900360640190fd5b34846305f5e1008210156118825760405162461bcd60e51b8152600401808060200182810382526026815260200180614cea6026913960400191505060405180910390fd5b61188a612dc9565b6118d0576040805162461bcd60e51b81526020600482015260126024820152712a37b79032b0b9363c903a3790323930bb9760711b604482015290519081900360640190fd5b6032601460006118de6127b1565b6001600160a01b031681526020810191909152604001600020541061190257600080fd5b611942878780806020026020016040519081016040528093929190818152602001838360200280828437600092019190915250899250349150612de89050565b50506003805461ff0019166101001790555050505050565b600581565b6015546060908190600160301b900465ffffffffffff1661197f57611adf565b601554601490600160301b900465ffffffffffff168111156119af5750601554600160301b900465ffffffffffff165b806040519080825280602002602001820160405280156119d9578160200160208202803883390190505b50915080604051908082528060200260200182016040528015611a06578160200160208202803883390190505b50925060005b818165ffffffffffff161015611adc5760155465ffffffffffff600160301b9091048116829003811660009081526011602052604090205485516001600160a01b03909116918691908416908110611a6057fe5b60200260200101906001600160a01b031690816001600160a01b0316815250506011600082601560069054906101000a900465ffffffffffff160365ffffffffffff16815260200190815260200160002060010154838265ffffffffffff1681518110611ac957fe5b6020908102919091010152600101611a0c565b50505b9091565b600354610100900460ff16611b2d576040805162461bcd60e51b815260206004820152601f6024820152600080516020614ca4833981519152604482015290519081900360640190fd5b6003805461ff0019169055620f42403411611b7f576040805162461bcd60e51b815260206004820152600d60248201526c09aeae6e840e6cadcc840a8a4b609b1b604482015290519081900360640190fd5b3460096000611b8c6127b1565b6001600160a01b031681526020810191909152604001600020805490910190556003805461ff001916610100179055565b611bc5611fbe565b611c04576040805162461bcd60e51b81526020600482018190526024820152600080516020614dbb833981519152604482015290519081900360640190fd5b61145660018263ffffffff6131be16565b611c1d611fbe565b611c5c576040805162461bcd60e51b81526020600482018190526024820152600080516020614dbb833981519152604482015290519081900360640190fd5b600080546040516001600160a01b03909116907f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e0908390a3600080546001600160a01b0319169055565b611cae611fbe565b611ced576040805162461bcd60e51b81526020600482018190526024820152600080516020614dbb833981519152604482015290519081900360640190fd5b61145660018263ffffffff612d4816565b60085461010090046001600160a01b031681565b611d1d6113e66127b1565b80611d2b5750611d2b611fbe565b611d665760405162461bcd60e51b8152600401808060200182810382526040815260200180614e2c6040913960400191505060405180910390fd5b600354610100900460ff16611db0576040805162461bcd60e51b815260206004820152601f6024820152600080516020614ca4833981519152604482015290519081900360640190fd5b6003805461ff00191690556000611dc56127b1565b9050803b8015611e10576040805162461bcd60e51b8152602060048201526011602482015270736f7272792068756d616e73206f6e6c7960781b604482015290519081900360640190fd5b611e186127b1565b6001600160a01b0316326001600160a01b031614611e72576040805162461bcd60e51b8152602060048201526012602482015271736f7272792c2068756d616e73206f6e6c7960701b604482015290519081900360640190fd5b50506006919091556007556003805461ff001916610100179055565b600a6020526000908152604090205460ff1681565b6000816040516020018082805190602001908083835b60208310611ed85780518252601f199092019160209182019101611eb9565b6001836020036101000a03801982511681845116808217855250505050505090500191505060405160208183030381529060405280519060200120836040516020018082805190602001908083835b60208310611f465780518252601f199092019160209182019101611f27565b6001836020036101000a038019825116818451168082178552505050505050905001915050604051602081830303815290604052805190602001201415611f8f57506001611f93565b5060005b92915050565b601e6020526000908152604090205460ff1681565b6000546001600160a01b03165b90565b600080546001600160a01b0316611fd36127b1565b6001600160a01b031614905090565b611fed6113e66127b1565b80611ffb5750611ffb611fbe565b6120365760405162461bcd60e51b8152600401808060200182810382526040815260200180614e2c6040913960400191505060405180910390fd5b61145660028263ffffffff6131be16565b600061205a60028363ffffffff61322516565b80611f935750611f93611fbe565b60035460ff1660011490565b61208461207f6127b1565b612047565b806120925750612092611fbe565b6120cd5760405162461bcd60e51b8152600401808060200182810382526040815260200180614e2c6040913960400191505060405180910390fd5b826018544203106120dd57600080fd5b610e10909202601955603c02601a55601c55565b6120fc6113e66127b1565b8061210a575061210a611fbe565b6121455760405162461bcd60e51b8152600401808060200182810382526040815260200180614e2c6040913960400191505060405180910390fd5b61214d61328c565b565b6121576149de565b61215f6149de565b60155460009061217e9065ffffffffffff16600163ffffffff6132cc16565b905060005b60008265ffffffffffff161180156121a15750600a8163ffffffff16105b156122045765ffffffffffff821660009081526010602052604081206121c9906002016132de565b6015549091508190859065ffffffffffff9081168690036000190116600a81106121ef57fe5b60200201525060001990910190600101612183565b509091505090565b60096020526000908152604090205481565b600061205a60018363ffffffff61322516565b61223c6113e66127b1565b8061224a575061224a611fbe565b6122855760405162461bcd60e51b8152600401808060200182810382526040815260200180614e2c6040913960400191505060405180910390fd5b60035460ff16156122dd576040805162461bcd60e51b815260206004820152601d60248201527f636f6e747261637420697320616c72656164792066696e616c697a6564000000604482015290519081900360640190fd5b60006122e76127b1565b9050803b8015612332576040805162461bcd60e51b8152602060048201526011602482015270736f7272792068756d616e73206f6e6c7960781b604482015290519081900360640190fd5b61233a6127b1565b6001600160a01b0316326001600160a01b031614612394576040805162461bcd60e51b8152602060048201526012602482015271736f7272792c2068756d616e73206f6e6c7960701b604482015290519081900360640190fd5b6123a561239f611fae565b47612ae4565b6123be6123b0611fae565b6001600160a01b0316611fbb565b6001600160a01b0316ff5b600354610100900460ff16612413576040805162461bcd60e51b815260206004820152601f6024820152600080516020614ca4833981519152604482015290519081900360640190fd5b6003805461ff0019169055600060098161242b6127b1565b6001600160a01b03166001600160a01b03168152602001908152602001600020541161245657600080fd5b600061248d600960006124676127b1565b6001600160a01b03166001600160a01b031681526020019081526020016000205461331e565b905060006009600061249d6127b1565b6001600160a01b031681526020810191909152604001600020556124c26114486127b1565b506003805461ff001916610100179055565b805160009082906124e95750600090506116c7565b50506020015190565b6012602052600090815260409020805460018201546002909201546001600160a01b03909116919065ffffffffffff80821691600160301b90041684565b612538614aed565b60035460ff1615612590576040805162461bcd60e51b815260206004820152601d60248201527f636f6e747261637420697320616c72656164792066696e616c697a6564000000604482015290519081900360640190fd5b60225481526023546020820152602454604082015290565b601460205281600052604060002081815481106125c157fe5b90600052602060002001600091509150505481565b6125de614b0b565b60606125e8614b2a565b601754835260155465ffffffffffff600160301b820481166020860152166040840152601854606084015261261b613367565b60808401526305f5e10060a084015264012a05f20060c0840152600a60e0840152601d54610100840152600061012084018190526101408401819052610160840181905261018084015261266d612812565b15158152612679612806565b15156020820152612688612dc9565b151560408201526000606082015261269e6129e9565b9150909192565b60035460ff16156126fd576040805162461bcd60e51b815260206004820152601d60248201527f636f6e747261637420697320616c72656164792066696e616c697a6564000000604482015290519081900360640190fd5b61214d61338d565b61270d611fbe565b61274c576040805162461bcd60e51b81526020600482018190526024820152600080516020614dbb833981519152604482015290519081900360640190fd5b611456816134ed565b6127606113e66127b1565b8061276e575061276e611fbe565b6127a95760405162461bcd60e51b8152600401808060200182810382526040815260200180614e2c6040913960400191505060405180910390fd5b61214d61358d565b3390565b600080805b83548110156127ff578381815481106127cf57fe5b60009182526020918290209181049091015460ff601f9092166101000a90041660020a91909101906001016127ba565b5092915050565b60195460185401421190565b600064012a05f2006017541015801561283e5750601554600a600160301b90910465ffffffffffff1610155b905090565b600080601360006128526127b1565b6001600160a01b0316815260208101919091526040016000205465ffffffffffff169050801580159061289a575060155465ffffffffffff600160301b909104811690821611155b80156128d057506128a96127b1565b65ffffffffffff82166000908152601160205260409020546001600160a01b039081169116145b91505090565b6128de6149de565b60006128ea84846135d5565b90506128f4614b48565b6128fc6149de565b60005b60328160ff1610156129305780838260ff166032811061291b57fe5b60ff90921660209290920201526001016128ff565b5060005b600a8110156129c657603281900360008165ffffffffffff6030850288901c168161295b57fe5b069050848160ff166032811061296d57fe5b60200201518484600a811061297e57fe5b60ff90921660209290920201528460001983016032811061299b57fe5b6020020151858260ff16603281106129af57fe5b60ff90921660209290920201525050600101612934565b5095945050505050565b6129d86149de565b6129e582600060096136f4565b5090565b601554606090600160301b900465ffffffffffff16612a0757611fbb565b601554600590600160301b900465ffffffffffff16811115612a375750601554600160301b900465ffffffffffff165b8065ffffffffffff16604051908082528060200260200182016040528015612a69578160200160208202803883390190505b50915060005b8165ffffffffffff168165ffffffffffff161015612adf5765ffffffffffff60018201811660009081526011602052604090205484516001600160a01b03909116918591908416908110612abf57fe5b6001600160a01b0390921660209283029190910190910152600101612a6f565b505090565b8015612b3657612afc826001600160a01b0316611fbb565b6001600160a01b03166108fc829081150290604051600060405180830381858888f19350505050158015612b34573d6000803e3d6000fd5b505b5050565b600b546000906001600160a01b03161580612b675750600b54612b65906001600160a01b0316613814565b155b15612b7657612b74613818565b505b600b546040805163bf40fac160e01b815260206004820181905260066024830152657075626c696360d01b604483015291516001600160a01b039093169263bf40fac1926064808401939192918290030181600087803b158015612bd957600080fd5b505af1158015612bed573d6000803e3d6000fd5b505050506040513d6020811015612c0357600080fd5b5051600c546001600160a01b03908116911614612cc957600b546040805163bf40fac160e01b815260206004820181905260066024830152657075626c696360d01b604483015291516001600160a01b039093169263bf40fac1926064808401939192918290030181600087803b158015612c7d57600080fd5b505af1158015612c91573d6000803e3d6000fd5b505050506040513d6020811015612ca757600080fd5b5051600c80546001600160a01b0319166001600160a01b039092169190911790555b600c60009054906101000a90046001600160a01b03166001600160a01b031663c281d19e6040518163ffffffff1660e01b815260040160206040518083038186803b158015612d1757600080fd5b505afa158015612d2b573d6000803e3d6000fd5b505050506040513d6020811015612d4157600080fd5b5051905090565b612d528282613225565b15612da4576040805162461bcd60e51b815260206004820152601f60248201527f526f6c65733a206163636f756e7420616c72656164792068617320726f6c6500604482015290519081900360640190fd5b6001600160a01b0316600090815260209190915260409020805460ff19166001179055565b60006018544211801561283e575050601a546019546018540103421090565b612e1c612e0d6064612e0184601963ffffffff61398416565b9063ffffffff6139a416565b6016549063ffffffff6139b916565b601655601754612e32908263ffffffff6139b916565b60175560146000612e416127b1565b6001600160a01b0316815260208082019290925260409081016000908120601d548154600181018355918352939091200191909155805160a0810190915280612e886127b1565b6001600160a01b039081168252601c5460208084019190915260155465ffffffffffff908116604080860182905260608087019290925260809586018a9052601d546000908152601285528190208751815496166001600160a01b0319909616959095178555868401516001860155860151600285018054928801518416600160301b026bffffffffffff000000000000199290941665ffffffffffff1990931692909217169190911790559183015180519192612f4e92600385019290910190614b67565b50905050612f6382612f5e6127b1565b6139c8565b15612fc8576000612f7b82600a63ffffffff6139a416565b9050612f878382612ae4565b6040805182815290516001600160a01b038516917fb81973cea7d4fc7b28d145a42eb998654da3af31e886111cea088fc89ca76b76919081900360200190a2505b612fd06127b1565b6001600160a01b03167fdbe8bd5a4c0db79169f073fabbf7f53e958b5f8694a446d645c07ab977b927b1826040518082815260200191505060405180910390a2601d805460010190556017805482019055600060138161302e6127b1565b6001600160a01b0316815260208101919091526040016000205460155465ffffffffffff9182169250600160301b900416811180613072575065ffffffffffff8116155b806130a857506130806127b1565b65ffffffffffff82166000908152601160205260409020546001600160a01b03908116911614155b156131975760158054600165ffffffffffff600160301b80840482169290920116026bffffffffffff0000000000001990911617905560408051808201909152806130f16127b1565b6001600160a01b039081168252602091820185905260158054600160301b9081900465ffffffffffff90811660009081526011865260408120875181546001600160a01b031916961695909517855595909401516001909301929092555404169060139061315d6127b1565b6001600160a01b031681526020810191909152604001600020805465ffffffffffff191665ffffffffffff929092169190911790556131b8565b65ffffffffffff811660009081526011602052604090206001018054830190555b50505050565b6131c88282613225565b6132035760405162461bcd60e51b8152600401808060200182810382526021815260200180614d5a6021913960400191505060405180910390fd5b6001600160a01b0316600090815260209190915260409020805460ff19169055565b60006001600160a01b03821661326c5760405162461bcd60e51b8152600401808060200182810382526022815260200180614ddb6022913960400191505060405180910390fd5b506001600160a01b03166000908152602091909152604090205460ff1690565b6003805460ff19169055604080516000815290517fd02d7ece1b390124a8d8d40fc59fc1d6584a261d9a503b71166ec69b3eef00b39181900360200190a1565b6000828211156132d857fe5b50900390565b600080805b600a8110156127ff578381600a81106132f857fe5b602081049091015460ff601f9092166101000a90041660020a91909101906001016132e3565b6000806133376064612e0185600563ffffffff61398416565b60055490915061334d908263ffffffff6139b916565b600555613360838263ffffffff6132cc16565b9392505050565b6018546019546000914291010381811215613386576000915050611fbb565b9050611fbb565b602554610100900460ff166133fc576133d96040518060400160405280600381526020016215549360ea1b815250604051806060016040528060408152602001614d7b60409139613a20565b601f8190556000908152601e60205260409020805460ff191660011790556134de565b60255460ff610100909104166001141561346f5761344d6040518060400160405280600381526020016215549360ea1b8152506040518060800160405280604a8152602001614d10604a9139613a20565b60208181556000918252601e905260409020805460ff191660011790556134de565b602554610100900460ff16600214156134de576134bf6040518060400160405280600381526020016215549360ea1b8152506040518060600160405280602f8152602001614dfd602f9139613a20565b60218190556000908152601e60205260409020805460ff191660011790555b6025805460ff19166003179055565b6001600160a01b0381166135325760405162461bcd60e51b8152600401808060200182810382526026815260200180614cc46026913960400191505060405180910390fd5b600080546040516001600160a01b03808516939216917f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e091a3600080546001600160a01b0319166001600160a01b0392909216919091179055565b6003805460ff1916600117908190556040805160ff929092168252517fd02d7ece1b390124a8d8d40fc59fc1d6584a261d9a503b71166ec69b3eef00b39181900360200190a1565b601754604080514342448181028302602080860182905284880184018688015296830260608087019190915241811b608087015288901b6001600160601b03191660948601528551808603608801815260a890950190955283519390950192909220601554600095939491908690600160301b900465ffffffffffff16828161365a57fe5b069050600061366882613bbd565b6025546022546023546024546040805160609690961b6001600160601b03191660208088019190915260f89590951b6001600160f81b03191660348701526035860199909952605585019e909e526075840191909152609583015260b58083019c909c528551808303909c018c5260d59091019094525050875197909101969096209695505050505050565b818180821415613705575050612b34565b6000856002868603058601600a811061371a57fe5b602002015160ff1690505b8183136137e6575b808684600a811061373a57fe5b602002015160ff1610156137535760019092019161372d565b8582600a811061375f57fe5b602002015160ff1681101561377a5760001990910190613753565b8183136137e1578582600a811061378d57fe5b60200201518684600a811061379e57fe5b60200201518785600a81106137af57fe5b602002018885600a81106137bf57fe5b60ff938416602091909102919091015291169052600190920191600019909101905b613725565b818512156137f9576137f98686846136f4565b8383121561380c5761380c8684866136f4565b505050505050565b3b90565b600080613838736457fbbf3ae193abac9b47b0809ff1af5236cd88613814565b111561389657600b80546001600160a01b031916736457fbbf3ae193abac9b47b0809ff1af5236cd88178155604080518082019091529081526a1d1c9e17db585a5b9b995d60aa1b602082015261388e90613bd8565b506001611fbb565b60006138b573292e33d054903bf949b779a7a11ab799006cc7ac613814565b111561390b57600b80546001600160a01b03191673292e33d054903bf949b779a7a11ab799006cc7ac17905560408051808201909152600a8152697472785f73686173746160b01b602082015261388e90613bd8565b600061392a7325069835b2e21df48552899a5cc61c840d6d0c1f613814565b111561397e57600b80546001600160a01b0319167325069835b2e21df48552899a5cc61c840d6d0c1f1790556040805180820190915260088152677472785f6e696c6560c01b602082015261388e90613bd8565b50600090565b600082820283158061399e57508284828161399b57fe5b04145b61336057fe5b6000808284816139b057fe5b04949350505050565b60008282018381101561336057fe5b6001600160a01b03821660009081526013602052604081205465ffffffffffff1615801590613a095750816001600160a01b0316836001600160a01b031614155b8015613360575050506001600160a01b0316151590565b600b546000906001600160a01b03161580613a4d5750600b54613a4b906001600160a01b0316613814565b155b15613a5c57613a5a613818565b505b600b546040805163bf40fac160e01b815260206004820181905260066024830152657075626c696360d01b604483015291516001600160a01b039093169263bf40fac1926064808401939192918290030181600087803b158015613abf57600080fd5b505af1158015613ad3573d6000803e3d6000fd5b505050506040513d6020811015613ae957600080fd5b5051600c546001600160a01b03908116911614613baf57600b546040805163bf40fac160e01b815260206004820181905260066024830152657075626c696360d01b604483015291516001600160a01b039093169263bf40fac1926064808401939192918290030181600087803b158015613b6357600080fd5b505af1158015613b77573d6000803e3d6000fd5b505050506040513d6020811015613b8d57600080fd5b5051600c80546001600160a01b0319166001600160a01b039092169190911790555b613360600084846000613beb565b6000908152601160205260409020546001600160a01b031690565b8051612b3690600d906020840190614bcd565b600080600c60009054906101000a90046001600160a01b03166001600160a01b0316634b94f50e6040518163ffffffff1660e01b8152600401602060405180830381600087803b158015613c3e57600080fd5b505af1158015613c52573d6000803e3d6000fd5b505050506040513d6020811015613c6857600080fd5b5051600b546040805163021fd35d60e31b815290519293506000926001600160a01b03909216916310fe9ae89160048082019260209290919082900301818787803b158015613cb657600080fd5b505af1158015613cca573d6000803e3d6000fd5b505050506040513d6020811015613ce057600080fd5b50519050831561438c57600c5460408051630bbceb3360e21b8152602481018790526004810191825288516044820152885160009384936001600160a01b0390911692632ef3accc928c928b92909182916064019060208601908083838c5b83811015613d57578181015183820152602001613d3f565b50505050905090810190601f168015613d845780820380516001836020036101000a031916815260200191505b5093505050506040805180830381600087803b158015613da357600080fd5b505af1158015613db7573d6000803e3d6000fd5b505050506040513d6040811015613dcd57600080fd5b508051602091820151600c5460408051636913553d60e01b815290519396509194506000936001600160a01b0390911692636913553d92600480820193929182900301818787803b158015613e2157600080fd5b505af1158015613e35573d6000803e3d6000fd5b505050506040513d6020811015613e4b57600080fd5b5051600a0a82860281613e5a57fe5b049050633b9aca00831115613e785750600094506149d69350505050565b600c60009054906101000a90046001600160a01b03166001600160a01b0316637edc9d4b6040518163ffffffff1660e01b815260040160206040518083038186803b158015613ec657600080fd5b505afa158015613eda573d6000803e3d6000fd5b505050506040513d6020811015613ef057600080fd5b50518015613f715750604080516370a0823160e01b8152306004820152905182916001600160a01b038716916370a0823191602480820192602092909190829003018186803b158015613f4257600080fd5b505afa158015613f56573d6000803e3d6000fd5b505050506040513d6020811015613f6c57600080fd5b505110155b1561430857600c5460408051636eb1769f60e11b81523060048201526001600160a01b0392831660248201529051839287169163dd62ed3e916044808301926020929190829003018186803b158015613fc957600080fd5b505afa158015613fdd573d6000803e3d6000fd5b505050506040513d6020811015613ff357600080fd5b50511061416957600c60009054906101000a90046001600160a01b03166001600160a01b0316638c954c3e60008c8c8c8c6040518663ffffffff1660e01b8152600401808581526020018060200180602001848152602001838103835286818151815260200191508051906020019080838360005b83811015614080578181015183820152602001614068565b50505050905090810190601f1680156140ad5780820380516001836020036101000a031916815260200191505b50838103825285518152855160209182019187019080838360005b838110156140e05781810151838201526020016140c8565b50505050905090810190601f16801561410d5780820380516001836020036101000a031916815260200191505b5096505050505050506020604051808303818588803b15801561412f57600080fd5b505af1158015614143573d6000803e3d6000fd5b50505050506040513d602081101561415a57600080fd5b505195506149d6945050505050565b600b546040805163bf40fac160e01b815260206004820181905260066024830152657075626c696360d01b604483015291516001600160a01b038089169463095ea7b39491169263bf40fac192606480830193928290030181600087803b1580156141d357600080fd5b505af11580156141e7573d6000803e3d6000fd5b505050506040513d60208110156141fd57600080fd5b5051604080516001600160e01b031960e085901b1681526001600160a01b03909216600483015260001960248301525160448083019260209291908290030181600087803b15801561424e57600080fd5b505af1158015614262573d6000803e3d6000fd5b505050506040513d602081101561427857600080fd5b505161428357600080fd5b600c60009054906101000a90046001600160a01b03166001600160a01b0316638c954c3e60008c8c8c8c6040518663ffffffff1660e01b81526004018085815260200180602001806020018481526020018381038352868181518152602001915080519060200190808383600083811015614080578181015183820152602001614068565b600c60009054906101000a90046001600160a01b03166001600160a01b0316638c954c3e848c8c8c8c6040518663ffffffff1660e01b81526004018085815260200180602001806020018481526020018381038352868181518152602001915080519060200190808383600083811015614080578181015183820152602001614068565b600c5460405163524f388960e01b815260206004820181815289516024840152895160009485946001600160a01b039091169363524f3889938d9390928392604490910191908501908083838b5b838110156143f25781810151838201526020016143da565b50505050905090810190601f16801561441f5780820380516001836020036101000a031916815260200191505b50925050506040805180830381600087803b15801561443d57600080fd5b505af1158015614451573d6000803e3d6000fd5b505050506040513d604081101561446757600080fd5b508051602091820151600c5460408051636913553d60e01b815290519396509194506000936001600160a01b0390911692636913553d92600480820193929182900301818787803b1580156144bb57600080fd5b505af11580156144cf573d6000803e3d6000fd5b505050506040513d60208110156144e557600080fd5b5051600a0a828602816144f457fe5b049050633b9aca008311156145125750600094506149d69350505050565b600c60009054906101000a90046001600160a01b03166001600160a01b0316637edc9d4b6040518163ffffffff1660e01b815260040160206040518083038186803b15801561456057600080fd5b505afa158015614574573d6000803e3d6000fd5b505050506040513d602081101561458a57600080fd5b5051801561460b5750604080516370a0823160e01b8152306004820152905182916001600160a01b038716916370a0823191602480820192602092909190829003018186803b1580156145dc57600080fd5b505afa1580156145f0573d6000803e3d6000fd5b505050506040513d602081101561460657600080fd5b505110155b1561495957600c5460408051636eb1769f60e11b81523060048201526001600160a01b0392831660248201529051839287169163dd62ed3e916044808301926020929190829003018186803b15801561466357600080fd5b505afa158015614677573d6000803e3d6000fd5b505050506040513d602081101561468d57600080fd5b5051106147c157600c60009054906101000a90046001600160a01b03166001600160a01b031663adf59f9960008c8c8c6040518563ffffffff1660e01b8152600401808481526020018060200180602001838103835285818151815260200191508051906020019080838360005b838110156147135781810151838201526020016146fb565b50505050905090810190601f1680156147405780820380516001836020036101000a031916815260200191505b50838103825284518152845160209182019186019080838360005b8381101561477357818101518382015260200161475b565b50505050905090810190601f1680156147a05780820380516001836020036101000a031916815260200191505b50955050505050506020604051808303818588803b15801561412f57600080fd5b600b546040805163bf40fac160e01b815260206004820181905260066024830152657075626c696360d01b604483015291516001600160a01b038089169463095ea7b39491169263bf40fac192606480830193928290030181600087803b15801561482b57600080fd5b505af115801561483f573d6000803e3d6000fd5b505050506040513d602081101561485557600080fd5b5051604080516001600160e01b031960e085901b1681526001600160a01b03909216600483015260001960248301525160448083019260209291908290030181600087803b1580156148a657600080fd5b505af11580156148ba573d6000803e3d6000fd5b505050506040513d60208110156148d057600080fd5b50516148db57600080fd5b600c60009054906101000a90046001600160a01b03166001600160a01b031663adf59f9960008c8c8c6040518563ffffffff1660e01b815260040180848152602001806020018060200183810383528581815181526020019150805190602001908083836000838110156147135781810151838201526020016146fb565b600c60009054906101000a90046001600160a01b03166001600160a01b031663adf59f99848c8c8c6040518563ffffffff1660e01b815260040180848152602001806020018060200183810383528581815181526020019150805190602001908083836000838110156147135781810151838201526020016146fb565b949350505050565b604051806101400160405280600a906020820280388339509192915050565b828054828255906000526020600020908101928215614a52579160200282015b82811115614a5257825182546001600160a01b0319166001600160a01b03909116178255602090920191600190910190614a1d565b506129e5929150614c47565b600183019183908215614ae15791602002820160005b83821115614ab257835183826101000a81548160ff021916908360ff1602179055509260200192600101602081600001049283019260010302614a74565b8015614adf5782816101000a81549060ff0219169055600101602081600001049283019260010302614ab2565b505b506129e5929150614c6b565b60405180606001604052806003906020820280388339509192915050565b604051806101a00160405280600d906020820280388339509192915050565b60405180608001604052806004906020820280388339509192915050565b6040518061064001604052806032906020820280388339509192915050565b82805482825590600052602060002090601f01602090048101928215614ae157916020028201600083821115614ab257835183826101000a81548160ff021916908360ff1602179055509260200192600101602081600001049283019260010302614a74565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f10614c0e57805160ff1916838001178555614c3b565b82800160010185558215614c3b579182015b82811115614c3b578251825591602001919060010190614c20565b506129e5929150614c89565b611fbb91905b808211156129e55780546001600160a01b0319168155600101614c4d565b611fbb91905b808211156129e557805460ff19168155600101614c71565b611fbb91905b808211156129e55760008155600101614c8f56fe5265656e7472616e637947756172643a207265656e7472616e742063616c6c004f776e61626c653a206e6577206f776e657220697320746865207a65726f20616464726573734d696e696d756d20616d6f756e7420746f20706c6179206973206e6f7420726561636865642e6a736f6e2868747470733a2f2f6170692e6b72616b656e2e636f6d2f302f7075626c69632f5469636b65723f706169723d545258555344292e726573756c742e5452585553442e612e30526f6c65733a206163636f756e7420646f6573206e6f74206861766520726f6c656a736f6e2868747470733a2f2f6170692e70726f2e636f696e626173652e636f6d2f70726f64756374732f4254432d5553442f7469636b6572292e70726963654f776e61626c653a2063616c6c6572206973206e6f7420746865206f776e6572526f6c65733a206163636f756e7420697320746865207a65726f20616464726573736a736f6e2868747470733a2f2f7777772e6269747374616d702e6e65742f6170692f7469636b65722f292e6c61737457686974656c69737441646d696e526f6c653a2063616c6c657220646f6573206e6f742068617665207468652057686974656c69737441646d696e20726f6c65a265627a7a72315820f8bb35c1c17e990a3c640fc25eb3f2a431dcde0a2cd1b66eaf942e6b6f42a5aa64736f6c634300050f0032";
TRC773.contractName = "TRC773";
