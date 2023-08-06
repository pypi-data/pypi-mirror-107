import { version, Contract } from "tronweb";
import BaseContract from "./base/base";
export class TRC757 extends BaseContract {
    constructor(tron) {
        super();
        this.__debug = true;
        this.tronweb = null;
        this.based_version = version;
        this.tronweb = tron;
    }
    static Instance() {
        if (window && window.hasOwnProperty("___contract__TRC757__")) {
            const obj = window.___contract__TRC757__;
            if (obj instanceof TRC757) {
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
        this.contract = await new Contract(this.tronweb, TRC757.ABI(), contract_address);
        this.contract_address_t = contract_address;
        if (window && !window.hasOwnProperty("___contract__TRC757__")) {
            window.___contract__TRC757__ = this;
        }
    }
    setDebug(bool) {
        this.__debug = bool;
    }
    isVersionCompatible() {
        return this.based_version === this.tronweb.version;
    }
    async ROULETTE_NUMBER_COUNT() {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0,
        };
        let val = await this.contract.ROULETTE_NUMBER_COUNT()
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 ROULETTE_NUMBER_COUNT");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async SERVICE_FEE() {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0,
        };
        let val = await this.contract.SERVICE_FEE()
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 SERVICE_FEE");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async TIMEOUT_FOR_BANK_REVEAL() {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0,
        };
        let val = await this.contract.TIMEOUT_FOR_BANK_REVEAL()
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 TIMEOUT_FOR_BANK_REVEAL");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async addWhitelistAdmin(account) {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0,
        };
        let val = await this.contract.addWhitelistAdmin(account)
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 addWhitelistAdmin");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async bankAddress() {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0,
        };
        let val = await this.contract.bankAddress()
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 bankAddress");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async checkBankSecretValueTimeout() {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0,
        };
        let val = await this.contract.checkBankSecretValueTimeout()
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 checkBankSecretValueTimeout");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async compareStr(src, src_compared) {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0,
        };
        let val = await this.contract.compareStr(src, src_compared)
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 compareStr");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async contractInvalidate() {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0,
        };
        let val = await this.contract.contractInvalidate()
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 contractInvalidate");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async depositFundsTrx(trx) {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: trx,
        };
        let val = await this.contract.depositFundsTrx()
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 depositFundsTrx");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async gameRounds(index_0) {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0,
        };
        let val = await this.contract.gameRounds(index_0)
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 gameRounds");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async hasRequestedGame(index_0) {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0,
        };
        let val = await this.contract.hasRequestedGame(index_0)
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 hasRequestedGame");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async initializeGame() {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0,
        };
        let val = await this.contract.initializeGame()
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 initializeGame");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async isGameRequested(user) {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0,
        };
        let val = await this.contract.isGameRequested(user)
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 isGameRequested");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async isHashReady(user) {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0,
        };
        let val = await this.contract.isHashReady(user)
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 isHashReady");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async isLocked() {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0,
        };
        let val = await this.contract.isLocked()
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 isLocked");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async isOwner() {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0,
        };
        let val = await this.contract.isOwner()
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 isOwner");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async isValueReady(user) {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0,
        };
        let val = await this.contract.isValueReady(user)
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 isValueReady");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async isWhitelistAdmin(account) {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0,
        };
        let val = await this.contract.isWhitelistAdmin(account)
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 isWhitelistAdmin");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async katana() {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0,
        };
        let val = await this.contract.katana()
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 katana");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async lock() {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0,
        };
        let val = await this.contract.lock()
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 lock");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async moveBankAddress() {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0,
        };
        let val = await this.contract.moveBankAddress()
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 moveBankAddress");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async owner() {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0,
        };
        let val = await this.contract.owner()
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 owner");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async placeBet(hasUserBetOnRed, userValue, _betAmount) {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0,
        };
        let val = await this.contract.placeBet(hasUserBetOnRed, userValue, _betAmount)
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 placeBet");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async registeredFunds(index_0) {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0,
        };
        let val = await this.contract.registeredFunds(index_0)
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 registeredFunds");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async removeWhitelistAdmin(account) {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0,
        };
        let val = await this.contract.removeWhitelistAdmin(account)
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 removeWhitelistAdmin");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async renounceOwnership() {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0,
        };
        let val = await this.contract.renounceOwnership()
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 renounceOwnership");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async sendBankSecretValue(bankSecretValue, nuhash, userAddress) {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0,
        };
        let val = await this.contract.sendBankSecretValue(bankSecretValue, nuhash, userAddress)
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 sendBankSecretValue");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async setInitialBankHash(bankHash, userAddress) {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0,
        };
        let val = await this.contract.setInitialBankHash(bankHash, userAddress)
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 setInitialBankHash");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async sphere_x() {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: true,
            callValue: 0,
        };
        let val = await this.contract.sphere_x()
            .call(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 sphere_x");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async transferOwnership(newOwner) {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0,
        };
        let val = await this.contract.transferOwnership(newOwner)
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 transferOwnership");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async unlock() {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0,
        };
        let val = await this.contract.unlock()
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 unlock");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async withdrawFundsTrx() {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0,
        };
        let val = await this.contract.withdrawFundsTrx()
            .send(callparams);
        if (this.__debug) {
            console.group("==> debug return raw 💮 withdrawFundsTrx");
            console.log(val);
            console.groupEnd();
        }
        return val;
    }
    async zjLimits(wtrx, sinktrx) {
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse: true,
            _isConstant: false,
            callValue: 0,
        };
        let val = await this.contract.zjLimits(wtrx, sinktrx)
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
        await this.contract && this.contract.GameResult().watch((err, event_payload) => {
            if (err)
                return console.error('Failed to bind event listener:', err);
            if (event_payload) {
                let { result, block, transaction, name, contract } = event_payload;
                if (this.__debug) {
                    console.group('New event received');
                    console.log('- Contract Address:', contract);
                    console.log('- Event Name:', name);
                    console.log('- Transaction:', transaction);
                    console.log('- Block number:', block);
                    console.log('- Result:', result, '\n');
                    console.groupEnd();
                }
                this.emit("event_GameResult", event_payload);
            }
        });
        await this.contract && this.contract.NewGameRequest().watch((err, event_payload) => {
            if (err)
                return console.error('Failed to bind event listener:', err);
            if (event_payload) {
                let { result, block, transaction, name, contract } = event_payload;
                if (this.__debug) {
                    console.group('New event received');
                    console.log('- Contract Address:', contract);
                    console.log('- Event Name:', name);
                    console.log('- Transaction:', transaction);
                    console.log('- Block number:', block);
                    console.log('- Result:', result, '\n');
                    console.groupEnd();
                }
                this.emit("event_NewGameRequest", event_payload);
            }
        });
        await this.contract && this.contract.OnBet().watch((err, event_payload) => {
            if (err)
                return console.error('Failed to bind event listener:', err);
            if (event_payload) {
                let { result, block, transaction, name, contract } = event_payload;
                if (this.__debug) {
                    console.group('New event received');
                    console.log('- Contract Address:', contract);
                    console.log('- Event Name:', name);
                    console.log('- Transaction:', transaction);
                    console.log('- Block number:', block);
                    console.log('- Result:', result, '\n');
                    console.groupEnd();
                }
                this.emit("event_OnBet", event_payload);
            }
        });
        await this.contract && this.contract.OwnershipTransferred().watch((err, event_payload) => {
            if (err)
                return console.error('Failed to bind event listener:', err);
            if (event_payload) {
                let { result, block, transaction, name, contract } = event_payload;
                if (this.__debug) {
                    console.group('New event received');
                    console.log('- Contract Address:', contract);
                    console.log('- Event Name:', name);
                    console.log('- Transaction:', transaction);
                    console.log('- Block number:', block);
                    console.log('- Result:', result, '\n');
                    console.groupEnd();
                }
                this.emit("event_OwnershipTransferred", event_payload);
            }
        });
        await this.contract && this.contract.traillock().watch((err, event_payload) => {
            if (err)
                return console.error('Failed to bind event listener:', err);
            if (event_payload) {
                let { result, block, transaction, name, contract } = event_payload;
                if (this.__debug) {
                    console.group('New event received');
                    console.log('- Contract Address:', contract);
                    console.log('- Event Name:', name);
                    console.log('- Transaction:', transaction);
                    console.log('- Block number:', block);
                    console.log('- Result:', result, '\n');
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
                stateMutability: 'nonpayable',
                type: 'constructor',
            },
            {
                anonymous: false,
                inputs: [
                    {
                        name: 'user',
                        type: 'address',
                        indexed: true,
                    },
                    {
                        name: 'gain',
                        type: 'uint256',
                        indexed: false,
                    },
                    {
                        name: 'loss',
                        type: 'uint256',
                        indexed: false,
                    },
                    {
                        name: 'result',
                        type: 'uint256',
                        indexed: false,
                    },
                ],
                name: 'GameResult',
                outputs: [],
                type: 'event',
            },
            {
                anonymous: false,
                inputs: [
                    {
                        name: 'user',
                        type: 'address',
                        indexed: true,
                    },
                ],
                name: 'NewGameRequest',
                outputs: [],
                type: 'event',
            },
            {
                anonymous: false,
                inputs: [
                    {
                        name: 'user',
                        type: 'address',
                        indexed: true,
                    },
                ],
                name: 'OnBet',
                outputs: [],
                type: 'event',
            },
            {
                anonymous: false,
                inputs: [
                    {
                        name: 'previousOwner',
                        type: 'address',
                        indexed: true,
                    },
                    {
                        name: 'newOwner',
                        type: 'address',
                        indexed: true,
                    },
                ],
                name: 'OwnershipTransferred',
                outputs: [],
                type: 'event',
            },
            {
                anonymous: false,
                inputs: [
                    {
                        name: 'value',
                        type: 'uint8',
                        indexed: false,
                    },
                ],
                name: 'traillock',
                outputs: [],
                type: 'event',
            },
            {
                inputs: [],
                outputs: [],
                payable: true,
                stateMutability: 'payable',
                type: 'fallback',
            },
            {
                constant: true,
                inputs: [],
                name: 'ROULETTE_NUMBER_COUNT',
                outputs: [
                    {
                        name: '',
                        type: 'uint256',
                    },
                ],
                payable: false,
                stateMutability: 'view',
                type: 'function',
            },
            {
                constant: true,
                inputs: [],
                name: 'SERVICE_FEE',
                outputs: [
                    {
                        name: '',
                        type: 'uint256',
                    },
                ],
                payable: false,
                stateMutability: 'view',
                type: 'function',
            },
            {
                constant: true,
                inputs: [],
                name: 'TIMEOUT_FOR_BANK_REVEAL',
                outputs: [
                    {
                        name: '',
                        type: 'uint256',
                    },
                ],
                payable: false,
                stateMutability: 'view',
                type: 'function',
            },
            {
                constant: false,
                inputs: [
                    {
                        name: 'account',
                        type: 'address',
                    },
                ],
                name: 'addWhitelistAdmin',
                outputs: [],
                payable: false,
                stateMutability: 'nonpayable',
                type: 'function',
            },
            {
                constant: true,
                inputs: [],
                name: 'bankAddress',
                outputs: [
                    {
                        name: '',
                        type: 'address',
                    },
                ],
                payable: false,
                stateMutability: 'view',
                type: 'function',
            },
            {
                constant: false,
                inputs: [],
                name: 'checkBankSecretValueTimeout',
                outputs: [],
                payable: false,
                stateMutability: 'nonpayable',
                type: 'function',
            },
            {
                constant: true,
                inputs: [
                    {
                        name: 'src',
                        type: 'string',
                    },
                    {
                        name: 'src_compared',
                        type: 'string',
                    },
                ],
                name: 'compareStr',
                outputs: [
                    {
                        name: '',
                        type: 'bool',
                    },
                ],
                payable: false,
                stateMutability: 'pure',
                type: 'function',
            },
            {
                constant: false,
                inputs: [],
                name: 'contractInvalidate',
                outputs: [],
                payable: false,
                stateMutability: 'nonpayable',
                type: 'function',
            },
            {
                constant: false,
                inputs: [],
                name: 'depositFundsTrx',
                outputs: [],
                payable: true,
                stateMutability: 'payable',
                type: 'function',
            },
            {
                constant: true,
                inputs: [
                    {
                        name: 'index_0',
                        type: 'address',
                    },
                ],
                name: 'gameRounds',
                outputs: [
                    {
                        name: 'bankHash',
                        type: 'bytes32',
                    },
                    {
                        name: 'bankSecretValue',
                        type: 'uint256',
                    },
                    {
                        name: 'userValue',
                        type: 'uint256',
                    },
                    {
                        name: 'timeWhenSecretUserValueSubmitted',
                        type: 'uint256',
                    },
                    {
                        name: 'lastGamePlayTime',
                        type: 'uint256',
                    },
                    {
                        name: 'lockedFunds',
                        type: 'uint256',
                    },
                    {
                        name: 'hasUserBetOnRed',
                        type: 'bool',
                    },
                ],
                payable: false,
                stateMutability: 'view',
                type: 'function',
            },
            {
                constant: true,
                inputs: [
                    {
                        name: 'index_0',
                        type: 'address',
                    },
                ],
                name: 'hasRequestedGame',
                outputs: [
                    {
                        name: '',
                        type: 'bool',
                    },
                ],
                payable: false,
                stateMutability: 'view',
                type: 'function',
            },
            {
                constant: false,
                inputs: [],
                name: 'initializeGame',
                outputs: [],
                payable: false,
                stateMutability: 'nonpayable',
                type: 'function',
            },
            {
                constant: true,
                inputs: [
                    {
                        name: 'user',
                        type: 'address',
                    },
                ],
                name: 'isGameRequested',
                outputs: [
                    {
                        name: '',
                        type: 'bool',
                    },
                ],
                payable: false,
                stateMutability: 'view',
                type: 'function',
            },
            {
                constant: true,
                inputs: [
                    {
                        name: 'user',
                        type: 'address',
                    },
                ],
                name: 'isHashReady',
                outputs: [
                    {
                        name: '',
                        type: 'bool',
                    },
                ],
                payable: false,
                stateMutability: 'view',
                type: 'function',
            },
            {
                constant: true,
                inputs: [],
                name: 'isLocked',
                outputs: [
                    {
                        name: '',
                        type: 'bool',
                    },
                ],
                payable: false,
                stateMutability: 'view',
                type: 'function',
            },
            {
                constant: true,
                inputs: [],
                name: 'isOwner',
                outputs: [
                    {
                        name: '',
                        type: 'bool',
                    },
                ],
                payable: false,
                stateMutability: 'view',
                type: 'function',
            },
            {
                constant: true,
                inputs: [
                    {
                        name: 'user',
                        type: 'address',
                    },
                ],
                name: 'isValueReady',
                outputs: [
                    {
                        name: '',
                        type: 'bool',
                    },
                ],
                payable: false,
                stateMutability: 'view',
                type: 'function',
            },
            {
                constant: true,
                inputs: [
                    {
                        name: 'account',
                        type: 'address',
                    },
                ],
                name: 'isWhitelistAdmin',
                outputs: [
                    {
                        name: '',
                        type: 'bool',
                    },
                ],
                payable: false,
                stateMutability: 'view',
                type: 'function',
            },
            {
                constant: false,
                inputs: [],
                name: 'katana',
                outputs: [],
                payable: false,
                stateMutability: 'nonpayable',
                type: 'function',
            },
            {
                constant: false,
                inputs: [],
                name: 'lock',
                outputs: [],
                payable: false,
                stateMutability: 'nonpayable',
                type: 'function',
            },
            {
                constant: false,
                inputs: [],
                name: 'moveBankAddress',
                outputs: [],
                payable: false,
                stateMutability: 'nonpayable',
                type: 'function',
            },
            {
                constant: true,
                inputs: [],
                name: 'owner',
                outputs: [
                    {
                        name: '',
                        type: 'address',
                    },
                ],
                payable: false,
                stateMutability: 'view',
                type: 'function',
            },
            {
                constant: false,
                inputs: [
                    {
                        name: 'hasUserBetOnRed',
                        type: 'bool',
                    },
                    {
                        name: 'userValue',
                        type: 'uint256',
                    },
                    {
                        name: '_betAmount',
                        type: 'uint256',
                    },
                ],
                name: 'placeBet',
                outputs: [],
                payable: false,
                stateMutability: 'nonpayable',
                type: 'function',
            },
            {
                constant: true,
                inputs: [
                    {
                        name: 'index_0',
                        type: 'address',
                    },
                ],
                name: 'registeredFunds',
                outputs: [
                    {
                        name: '',
                        type: 'uint256',
                    },
                ],
                payable: false,
                stateMutability: 'view',
                type: 'function',
            },
            {
                constant: false,
                inputs: [
                    {
                        name: 'account',
                        type: 'address',
                    },
                ],
                name: 'removeWhitelistAdmin',
                outputs: [],
                payable: false,
                stateMutability: 'nonpayable',
                type: 'function',
            },
            {
                constant: false,
                inputs: [],
                name: 'renounceOwnership',
                outputs: [],
                payable: false,
                stateMutability: 'nonpayable',
                type: 'function',
            },
            {
                constant: false,
                inputs: [
                    {
                        name: 'bankSecretValue',
                        type: 'uint256',
                    },
                    {
                        name: 'nuhash',
                        type: 'bytes32',
                    },
                    {
                        name: 'userAddress',
                        type: 'address',
                    },
                ],
                name: 'sendBankSecretValue',
                outputs: [],
                payable: false,
                stateMutability: 'nonpayable',
                type: 'function',
            },
            {
                constant: false,
                inputs: [
                    {
                        name: 'bankHash',
                        type: 'bytes32',
                    },
                    {
                        name: 'userAddress',
                        type: 'address',
                    },
                ],
                name: 'setInitialBankHash',
                outputs: [],
                payable: false,
                stateMutability: 'nonpayable',
                type: 'function',
            },
            {
                constant: true,
                inputs: [],
                name: 'sphere_x',
                outputs: [
                    {
                        name: 'wallet',
                        type: 'uint256[8]',
                    },
                    {
                        name: 'hash',
                        type: 'bytes32',
                    },
                    {
                        name: 'hFlags',
                        type: 'bool[3]',
                    },
                    {
                        name: 'mcInfo',
                        type: 'uint256[6]',
                    },
                ],
                payable: false,
                stateMutability: 'view',
                type: 'function',
            },
            {
                constant: false,
                inputs: [
                    {
                        name: 'newOwner',
                        type: 'address',
                    },
                ],
                name: 'transferOwnership',
                outputs: [],
                payable: false,
                stateMutability: 'nonpayable',
                type: 'function',
            },
            {
                constant: false,
                inputs: [],
                name: 'unlock',
                outputs: [],
                payable: false,
                stateMutability: 'nonpayable',
                type: 'function',
            },
            {
                constant: false,
                inputs: [],
                name: 'withdrawFundsTrx',
                outputs: [],
                payable: false,
                stateMutability: 'nonpayable',
                type: 'function',
            },
            {
                constant: false,
                inputs: [
                    {
                        name: 'wtrx',
                        type: 'uint256',
                    },
                    {
                        name: 'sinktrx',
                        type: 'uint256',
                    },
                ],
                name: 'zjLimits',
                outputs: [],
                payable: false,
                stateMutability: 'nonpayable',
                type: 'function',
            },
        ];
        return abi;
    }
}
TRC757.deployedBytecode = "60806040526002805461ff01600160b01b03191675a5576e55542477ce999f2d3a8c242697b0fcf41600001790556003805473a5576e55542477ce999f2d3a8c242697b0fcf4166001600160a01b0319909116179055600060045562000077620f424061271062000275602090811b6200278217901c565b600555620000996103e8620f42406200027560201b620027821790919060201c565b6006556007805460ff19169055604080516104a0810182526000808252600160208301819052928201819052606082018390526080820181905260a0820183905260c0820181905260e08201839052610100820181905261012082018390526101408201819052610160820181905261018082018390526101a082018190526101c082018390526101e08201819052610200820183905261022082018190526102408201839052610260820183905261028082018190526102a082018390526102c082018190526102e08201839052610300820181905261032082018390526103408201819052610360820183905261038082018190526103a082018190526103c082018390526103e08201819052610400820183905261042082018190526104408201839052610460820152610480810191909152620001df90600b906025620002df565b50348015620001ed57600080fd5b506000620002036001600160e01b036200029f16565b600080546001600160a01b0319166001600160a01b0383169081178255604051929350917f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e0908290a3506002805461ff0019166101001790556200026f6001600160e01b03620002a416565b62000399565b6000828202831580620002915750828482816200028e57fe5b04145b6200029857fe5b9392505050565b335b90565b620002b76001600160e01b036200029f16565b600760016101000a8154816001600160a01b0302191690836001600160a01b03160217905550565b600283019183908215620003665791602002820160005b838211156200033557835183826101000a81548160ff0219169083151502179055509260200192600101602081600001049283019260010302620002f6565b8015620003645782816101000a81549060ff021916905560010160208160000104928301926001030262000335565b505b506200037492915062000378565b5090565b620002a191905b808211156200037457805460ff191681556001016200037f565b6129a480620003a96000396000f3fe6080604052600436106101ee5760003560e01c806387c5d5cc1161010d578063ab63e6fb116100a0578063c59974191161006f578063c5997419146107e4578063e1f0c1c1146107f9578063f2fde38b1461082c578063f83d08ba1461085f578063fe68848914610874576101ee565b8063ab63e6fb1461072a578063b3a5cec614610769578063bb5f747b1461079c578063bc7e9c5c146107cf576101ee565b8063a0a1f49b116100dc578063a0a1f49b146106d6578063a35fdf95146106eb578063a4e2d63414610700578063a69df4b514610715576101ee565b806387c5d5cc1461055d5780638da5cb5b146106975780638f32d59b146106ac5780639dc77d58146106c1576101ee565b80636897e974116101855780637826d064116101545780637826d0641461048e5780637f02d905146104be57806384ac6ae5146104f157806384ba9eaf14610524576101ee565b80636897e974146103e2578063715018a6146104155780637362d9c81461042a5780637822ed491461045d576101ee565b80632d8f3ad8116101c15780632d8f3ad81461029957806350c86de51461034657806361ff6e641461036d57806364ea957614610375576101ee565b806302991f49146101f057806303ee0bdc146102375780630c64589d1461024c5780631e00c5a514610261575b005b3480156101fc57600080fd5b506102236004803603602081101561021357600080fd5b50356001600160a01b0316610889565b604080519115158252519081900360200190f35b34801561024357600080fd5b506101ee61090a565b34801561025857600080fd5b506101ee610bdd565b34801561026d57600080fd5b506101ee6004803603606081101561028457600080fd5b50803515159060208101359060400135610c56565b3480156102a557600080fd5b506102ae610edd565b604051808561010080838360005b838110156102d45781810151838201526020016102bc565b5050505090500184815260200183600360200280838360005b838110156103055781810151838201526020016102ed565b5050505090500182600660200280838360005b83811015610330578181015183820152602001610318565b5050505090500194505050505060405180910390f35b34801561035257600080fd5b5061035b610f15565b60408051918252519081900360200190f35b6101ee610f1a565b34801561038157600080fd5b506103a86004803603602081101561039857600080fd5b50356001600160a01b0316610ff4565b604080519788526020880196909652868601949094526060860192909252608085015260a0840152151560c0830152519081900360e00190f35b3480156103ee57600080fd5b506101ee6004803603602081101561040557600080fd5b50356001600160a01b0316611034565b34801561042157600080fd5b506101ee61108c565b34801561043657600080fd5b506101ee6004803603602081101561044d57600080fd5b50356001600160a01b031661111d565b34801561046957600080fd5b50610472611175565b604080516001600160a01b039092168252519081900360200190f35b34801561049a57600080fd5b506101ee600480360360408110156104b157600080fd5b5080359060200135611189565b3480156104ca57600080fd5b50610223600480360360208110156104e157600080fd5b50356001600160a01b0316611305565b3480156104fd57600080fd5b506102236004803603602081101561051457600080fd5b50356001600160a01b031661131a565b34801561053057600080fd5b506101ee6004803603604081101561054757600080fd5b50803590602001356001600160a01b0316611396565b34801561056957600080fd5b506102236004803603604081101561058057600080fd5b81019060208101813564010000000081111561059b57600080fd5b8201836020820111156105ad57600080fd5b803590602001918460018302840111640100000000831117156105cf57600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600092019190915250929594936020810193503591505064010000000081111561062257600080fd5b82018360208201111561063457600080fd5b8035906020019184600183028401116401000000008311171561065657600080fd5b91908080601f0160208091040260200160405190810160405280939291908181526020018383808284376000920191909152509295506113f8945050505050565b3480156106a357600080fd5b506104726114ee565b3480156106b857600080fd5b506102236114fd565b3480156106cd57600080fd5b5061035b611521565b3480156106e257600080fd5b506101ee611528565b3480156106f757600080fd5b506101ee6116c5565b34801561070c57600080fd5b506102236118fb565b34801561072157600080fd5b506101ee611907565b34801561073657600080fd5b506101ee6004803603606081101561074d57600080fd5b50803590602081013590604001356001600160a01b0316611965565b34801561077557600080fd5b5061035b6004803603602081101561078c57600080fd5b50356001600160a01b0316611af5565b3480156107a857600080fd5b50610223600480360360208110156107bf57600080fd5b50356001600160a01b0316611b07565b3480156107db57600080fd5b506101ee611b28565b3480156107f057600080fd5b506101ee611cc0565b34801561080557600080fd5b506102236004803603602081101561081c57600080fd5b50356001600160a01b0316611e31565b34801561083857600080fd5b506101ee6004803603602081101561084f57600080fd5b50356001600160a01b0316611e4f565b34801561086b57600080fd5b506101ee611e9f565b34801561088057600080fd5b5061035b611efb565b60006108936127c6565b50506001600160a01b03166000908152600a6020908152604091829020825160e08101845281548082526001830154938201939093526002820154938101939093526003810154606084015260048101546080840152600581015460a08401526006015460ff16151560c090920191909152151590565b61091a610915611f00565b611b07565b8061092857506109286114fd565b6109635760405162461bcd60e51b81526004018080602001828103825260408152602001806129306040913960400191505060405180910390fd5b600061096d611f00565b9050803b80156109b8576040805162461bcd60e51b8152602060048201526011602482015270736f7272792068756d616e73206f6e6c7960781b604482015290519081900360640190fd5b6109c0611f00565b6001600160a01b0316326001600160a01b031614610a1a576040805162461bcd60e51b8152602060048201526012602482015271736f7272792c2068756d616e73206f6e6c7960701b604482015290519081900360640190fd5b600254610100900460ff16610a64576040805162461bcd60e51b815260206004820152601f6024820152600080516020612864833981519152604482015290519081900360640190fd5b6002805461ff001916905560075461010090046001600160a01b0316600090815260086020819052604082205491829190610a9d611f00565b6001600160a01b03168152602081019190915260400160002055610abf6127c6565b5060075461010090046001600160a01b03166000908152600a60208181526040808420815160e081018352815481526001820154938101939093526002810154918301919091526003810154606083015260048101546080830152600581015460a08301526006015460ff16151560c0820152919081610b3d611f00565b6001600160a01b0316815260208082019290925260409081016000208451815590840151600282015560a0840151600582015590830151600182015560c083015160068201805460ff1916911515919091179055606083015160038201559050610ba5611f00565b60078054610100600160a81b0319166101006001600160a01b039390931683021790556002805461ff00191690911790555050505050565b610be8610915611f00565b80610bf65750610bf66114fd565b610c315760405162461bcd60e51b81526004018080602001828103825260408152602001806129306040913960400191505060405180910390fd5b600480546000909155610c4b610c45611f00565b82611f04565b610c53611963565b50565b600a6000610c62611f00565b6001600160a01b03168152602081019190915260400160002054610cc5576040805162461bcd60e51b815260206004820152601560248201527410985b9ac81a185cda081b9bdd081e595d081cd95d605a1b604482015290519081900360640190fd5b600a6000610cd1611f00565b6001600160a01b0316815260208101919091526040016000206002015415610d35576040805162461bcd60e51b8152602060048201526012602482015271105b1c9958591e481c1b1858d9590818995d60721b604482015290519081900360640190fd5b80610d3e611f59565b1015610d89576040805162461bcd60e51b81526020600482015260156024820152744e6f7420656e6f7567682062616e6b2066756e647360581b604482015290519081900360640190fd5b80610d9a610d95611f00565b611faf565b1015610de5576040805162461bcd60e51b81526020600482015260156024820152744e6f7420656e6f75676820757365722066756e647360581b604482015290519081900360640190fd5b81600a6000610df2611f00565b6001600160a01b03166001600160a01b031681526020019081526020016000206002018190555082600a6000610e26611f00565b6001600160a01b03166001600160a01b0316815260200190815260200160002060060160006101000a81548160ff02191690831515021790555042600a6000610e6d611f00565b6001600160a01b03168152602081019190915260400160002060030155610e9b610e95611f00565b82611fed565b610ea3611f00565b6001600160a01b03167fd588cb1d41de6084c93e2df965e503ad46eed106265a9fbb1c0d77adb4d47f5e60405160405180910390a2505050565b610ee5612808565b6000610eef612827565b610ef7612845565b610f07610f02611f00565b612027565b935093509350935090919293565b600581565b600254610100900460ff16610f64576040805162461bcd60e51b815260206004820152601f6024820152600080516020612864833981519152604482015290519081900360640190fd5b6002805461ff0019169055620f42403411610fb6576040805162461bcd60e51b815260206004820152600d60248201526c09aeae6e840e6cadcc840a8a4b609b1b604482015290519081900360640190fd5b3460086000610fc3611f00565b6001600160a01b031681526020810191909152604001600020805490910190556002805461ff001916610100179055565b600a602052600090815260409020805460018201546002830154600384015460048501546005860154600690960154949593949293919290919060ff1687565b61103c6114fd565b61107b576040805162461bcd60e51b815260206004820181905260248201526000805160206128ee833981519152604482015290519081900360640190fd5b610c5360018263ffffffff6121a516565b6110946114fd565b6110d3576040805162461bcd60e51b815260206004820181905260248201526000805160206128ee833981519152604482015290519081900360640190fd5b600080546040516001600160a01b03909116907f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e0908390a3600080546001600160a01b0319169055565b6111256114fd565b611164576040805162461bcd60e51b815260206004820181905260248201526000805160206128ee833981519152604482015290519081900360640190fd5b610c5360018263ffffffff61220c16565b60075461010090046001600160a01b031681565b611194610915611f00565b806111a257506111a26114fd565b6111dd5760405162461bcd60e51b81526004018080602001828103825260408152602001806129306040913960400191505060405180910390fd5b600254610100900460ff16611227576040805162461bcd60e51b815260206004820152601f6024820152600080516020612864833981519152604482015290519081900360640190fd5b6002805461ff0019169055600061123c611f00565b9050803b8015611287576040805162461bcd60e51b8152602060048201526011602482015270736f7272792068756d616e73206f6e6c7960781b604482015290519081900360640190fd5b61128f611f00565b6001600160a01b0316326001600160a01b0316146112e9576040805162461bcd60e51b8152602060048201526012602482015271736f7272792c2068756d616e73206f6e6c7960701b604482015290519081900360640190fd5b50506005919091556006556002805461ff001916610100179055565b60096020526000908152604090205460ff1681565b60006113246127c6565b50506001600160a01b03166000908152600a6020908152604091829020825160e0810184528154815260018201549281019290925260028101549282018390526003810154606083015260048101546080830152600581015460a08301526006015460ff16151560c090910152151590565b6113a1610915611f00565b806113af57506113af6114fd565b6113ea5760405162461bcd60e51b81526004018080602001828103825260408152602001806129306040913960400191505060405180910390fd5b6113f4828261228d565b5050565b6000816040516020018082805190602001908083835b6020831061142d5780518252601f19909201916020918201910161140e565b6001836020036101000a03801982511681845116808217855250505050505090500191505060405160208183030381529060405280519060200120836040516020018082805190602001908083835b6020831061149b5780518252601f19909201916020918201910161147c565b6001836020036101000a0380198251168184511680821785525050505050509050019150506040516020818303038152906040528051906020012014156114e4575060016114e8565b5060005b92915050565b6000546001600160a01b031690565b600080546001600160a01b0316611512611f00565b6001600160a01b031614905090565b6201518081565b6000611532611f00565b9050803b801561157d576040805162461bcd60e51b8152602060048201526011602482015270736f7272792068756d616e73206f6e6c7960781b604482015290519081900360640190fd5b611585611f00565b6001600160a01b0316326001600160a01b0316146115df576040805162461bcd60e51b8152602060048201526012602482015271736f7272792c2068756d616e73206f6e6c7960701b604482015290519081900360640190fd5b600960006115eb611f00565b6001600160a01b0316815260208101919091526040016000205460ff161561164e576040805162461bcd60e51b8152602060048201526011602482015270105b1c9958591e481c995c5d595cdd1959607a1b604482015290519081900360640190fd5b60016009600061165c611f00565b6001600160a01b031681526020810191909152604001600020805460ff191691151591909117905561168c611f00565b6001600160a01b03167f2ecaf1493a770f6567e43ff54567b68042dd048a3cfb2f07359a89286913d30d60405160405180910390a25050565b6116cd6127c6565b600a60006116d9611f00565b6001600160a01b031681526020808201929092526040908101600020815160e08101835281548082526001830154948201949094526002820154928101929092526003810154606083015260048101546080830152600581015460a08301526006015460ff16151560c0820152915061178d576040805162461bcd60e51b815260206004820152601160248201527010985b9ac81a185cda081b9bdd081cd95d607a1b604482015290519081900360640190fd5b6020810151156117d9576040805162461bcd60e51b815260206004820152601260248201527110985b9ac81cd958dc995d081a5cc81cd95d60721b604482015290519081900360640190fd5b6040810151611824576040805162461bcd60e51b8152602060048201526012602482015271155cd95c881d985b1d59481b9bdd081cd95d60721b604482015290519081900360640190fd5b60608101516201518001428110611882576040805162461bcd60e51b815260206004820152601760248201527f54696d656f7574206e6f74207965742072656163686564000000000000000000604482015290519081900360640190fd5b60a082015160075461010090046001600160a01b03166000908152600a6020526040902060050180549190910390556118c16118bc611f00565b61230a565b6000600960006118cf611f00565b6001600160a01b031681526020810191909152604001600020805460ff19169115159190911790555050565b60025460ff1660011490565b611912610915611f00565b8061192057506119206114fd565b61195b5760405162461bcd60e51b81526004018080602001828103825260408152602001806129306040913960400191505060405180910390fd5b611963612398565b565b6001600160a01b0381166000908152600a60205260409020600201546119ca576040805162461bcd60e51b8152602060048201526015602482015274155cd95c881a185cc81b9bc81d985b1d59481cd95d605a1b604482015290519081900360640190fd5b6001600160a01b0381166000908152600a602052604090206001015415611a2b576040805162461bcd60e51b815260206004820152601060248201526f105b1c9958591e481c995d99585b195960821b604482015290519081900360640190fd5b60408051602080820186905282518083038201815291830183528151918101919091206001600160a01b0384166000908152600a909252919020548114611aa35760405162461bcd60e51b81526004018080602001828103825260238152602001806128cb6023913960400191505060405180910390fd5b6001600160a01b0382166000908152600a60205260409020600101849055611aca826123d8565b611ad38261230a565b506001600160a01b03166000908152600a602052604090204260048201555550565b60086020526000908152604090205481565b6000611b1a60018363ffffffff61259e16565b806114e857506114e86114fd565b611b33610915611f00565b80611b415750611b416114fd565b611b7c5760405162461bcd60e51b81526004018080602001828103825260408152602001806129306040913960400191505060405180910390fd5b60025460ff1615611bd4576040805162461bcd60e51b815260206004820152601d60248201527f636f6e747261637420697320616c72656164792066696e616c697a6564000000604482015290519081900360640190fd5b6000611bde611f00565b9050803b8015611c29576040805162461bcd60e51b8152602060048201526011602482015270736f7272792068756d616e73206f6e6c7960781b604482015290519081900360640190fd5b611c31611f00565b6001600160a01b0316326001600160a01b031614611c8b576040805162461bcd60e51b8152602060048201526012602482015271736f7272792c2068756d616e73206f6e6c7960701b604482015290519081900360640190fd5b611c9c611c966114ee565b47611f04565b611cb5611ca76114ee565b6001600160a01b0316612605565b6001600160a01b0316ff5b600254610100900460ff16611d0a576040805162461bcd60e51b815260206004820152601f6024820152600080516020612864833981519152604482015290519081900360640190fd5b6002805461ff00191690556000600881611d22611f00565b6001600160a01b03166001600160a01b031681526020019081526020016000205411611d4d57600080fd5b600a6000611d59611f00565b6001600160a01b0316815260208101919091526040016000206005015415611d8057600080fd5b600a6000611d8c611f00565b6001600160a01b0316815260208101919091526040016000206003015415611db357600080fd5b6000611dea60086000611dc4611f00565b6001600160a01b03166001600160a01b0316815260200190815260200160002054612608565b9050600060086000611dfa611f00565b6001600160a01b03168152602081019190915260400160002055611e1f610c45611f00565b506002805461ff001916610100179055565b6001600160a01b031660009081526009602052604090205460ff1690565b611e576114fd565b611e96576040805162461bcd60e51b815260206004820181905260248201526000805160206128ee833981519152604482015290519081900360640190fd5b610c5381612656565b611eaa610915611f00565b80611eb85750611eb86114fd565b611ef35760405162461bcd60e51b81526004018080602001828103825260408152602001806129306040913960400191505060405180910390fd5b6119636126f6565b602581565b3390565b80156113f457611f1c826001600160a01b0316612605565b6001600160a01b03166108fc829081150290604051600060405180830381858888f19350505050158015611f54573d6000803e3d6000fd5b505050565b60075461010090046001600160a01b03166000908152600a60209081526040808320600501546004546008909352908320549091611fa9918391611f9d919061273e565b9063ffffffff61273e16565b91505090565b6001600160a01b0381166000908152600a60209081526040808320600501546008909252822054611fe6908263ffffffff61273e16565b9392505050565b6007546001600160a01b0361010090910481166000908152600a602052604080822060059081018054860190559490921681522090910155565b61202f612808565b6000612039612827565b612041612845565b6120496127c6565b506001600160a01b0385166000908152600a6020908152604091829020825160e081018452815481526001820154928101929092526002810154928201929092526003820154606082015260048201546080820152600582015460a082015260069091015460ff16151560c082018190526120c55760006120c8565b60015b60ff168552602081810151908601526040808201519086015260a08101516060808701919091528101516080860152612102610d95611f00565b60a0860152600060c0860152608081015160e08601526121218661131a565b1515835261212e86610889565b1515602084015261213e86611e31565b15156040808501919091526201518083526025602084015260045490830152612165611f59565b606083015260075461010090046001600160a01b03166000908152600a602052604090206005015460808301524260a08301525193959394509092909150565b6121af828261259e565b6121ea5760405162461bcd60e51b81526004018080602001828103825260218152602001806128aa6021913960400191505060405180910390fd5b6001600160a01b0316600090815260209190915260409020805460ff19169055565b612216828261259e565b15612268576040805162461bcd60e51b815260206004820152601f60248201527f526f6c65733a206163636f756e7420616c72656164792068617320726f6c6500604482015290519081900360640190fd5b6001600160a01b0316600090815260209190915260409020805460ff19166001179055565b6001600160a01b0381166000908152600a6020526040902054156122f0576040805162461bcd60e51b815260206004820152601560248201527410985b9ac81a185cda08185b1c9958591e481cd95d605a1b604482015290519081900360640190fd5b6001600160a01b03166000908152600a6020526040902055565b6040805160e08101825260008082526020808301828152838501838152606085018481526080860185815260a0870186815260c088018781526001600160a01b039a909a168752600a90955296909420945185559051600185015551600284015590516003830155915160048201559051600582015590516006909101805460ff1916911515919091179055565b6002805460ff19169055604080516000815290517fd02d7ece1b390124a8d8d40fc59fc1d6584a261d9a503b71166ec69b3eef00b39181900360200190a1565b6001600160a01b0381166000908152600a602052604081206002810154600182015460059092015491189160258084069291829184159190600b908690811061241d57fe5b6020808204909201546001600160a01b038a166000908152600a909352604083206006015460ff601f9093166101000a90910482169350169080841561247657505060075461010090046001600160a01b0316886124b1565b821515841515141561249c575050600754889061010090046001600160a01b03166124b1565b505060075461010090046001600160a01b0316885b6124bc828288612750565b6007546001600160a01b0361010090910481166000908152600a6020526040902060050180548990039055828116908b1614156125445760408051878152600060208201528082018a905290516001600160a01b038c16917fb23ab49b4ba9602e729f07366027f225f26e664a9cfec60a5ed4cbf87a81fb04919081900360600190a2612592565b6040805160008152602081018890528082018a905290516001600160a01b038c16917fb23ab49b4ba9602e729f07366027f225f26e664a9cfec60a5ed4cbf87a81fb04919081900360600190a25b50505050505050505050565b60006001600160a01b0382166125e55760405162461bcd60e51b815260040180806020018281038252602281526020018061290e6022913960400191505060405180910390fd5b506001600160a01b03166000908152602091909152604090205460ff1690565b90565b60008061262d606461262185600563ffffffff61278216565b9063ffffffff6127a216565b600454909150612643908263ffffffff6127b716565b600455611fe6838263ffffffff61273e16565b6001600160a01b03811661269b5760405162461bcd60e51b81526004018080602001828103825260268152602001806128846026913960400191505060405180910390fd5b600080546040516001600160a01b03808516939216917f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e091a3600080546001600160a01b0319166001600160a01b0392909216919091179055565b6002805460ff1916600117908190556040805160ff929092168252517fd02d7ece1b390124a8d8d40fc59fc1d6584a261d9a503b71166ec69b3eef00b39181900360200190a1565b60008282111561274a57fe5b50900390565b6001600160a01b0392831660009081526008602052604080822080548401905592909316835291208054919091039055565b600082820283158061279c57508284828161279957fe5b04145b611fe657fe5b6000808284816127ae57fe5b04949350505050565b600082820183811015611fe657fe5b6040518060e001604052806000801916815260200160008152602001600081526020016000815260200160008152602001600081526020016000151581525090565b6040518061010001604052806008906020820280388339509192915050565b60405180606001604052806003906020820280388339509192915050565b6040518060c00160405280600690602082028038833950919291505056fe5265656e7472616e637947756172643a207265656e7472616e742063616c6c004f776e61626c653a206e6577206f776e657220697320746865207a65726f2061646472657373526f6c65733a206163636f756e7420646f6573206e6f74206861766520726f6c6542616e6b2072657665616c206e6f74206d61746368696e6720636f6d6d69746d656e744f776e61626c653a2063616c6c6572206973206e6f7420746865206f776e6572526f6c65733a206163636f756e7420697320746865207a65726f206164647265737357686974656c69737441646d696e526f6c653a2063616c6c657220646f6573206e6f742068617665207468652057686974656c69737441646d696e20726f6c65a265627a7a723158207cb45e4bbedf1085d1a645746101bc9e5f09fb90c8da5552ee84678fee02a6d464736f6c63430005100032";
TRC757.contractName = "TRC757";
