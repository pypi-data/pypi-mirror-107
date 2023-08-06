/* DO NOT EDIT THE BELOW FILE AS THIS IS LIKELY WILL BE GENERATED AGAIN AND REWRITE OVER IT */
// tslint:disable:no-consecutive-blank-lines ordered-imports align trailing-comma enum-naming
// tslint:disable:whitespace no-unbound-method no-trailing-whitespace no-camelcase
// tslint:disable:no-unused-variable
import TronWeb, {BigNumber, version, Contract} from "tronweb"
import BaseContract from "./base/base"
import {ReqEventResult} from "abi/base/types";
// eslint-disable-next-line import/named

type Param = {
    type: string,
    value: any
}

export interface ContractInterface {
    commission(amount: string, ticket_buyer: string):Promise<void>
    compareStr(src: string, src_compared: string):Promise<boolean>
    drain():Promise<void>
    genesisRegistration(me: string):Promise<void>
    getMyDat():Promise<BigNumber[]>
    isExist(check: string):Promise<boolean>
    registerFast(upperline: string):Promise<void>
    registerName(me: string, upperline: string):Promise<void>
    seeTokenAddress():Promise<string>
    setAssetToken(address_loc: string):Promise<void>
}

// @ts-ignore
export class Network extends BaseContract implements ContractInterface {

public static deployedBytecode = "6080604052610bb7806100136000396000f3fe608060405234801561001057600080fd5b506004361061009d5760003560e01c806387c5d5cc1161006657806387c5d5cc146101985780638fc44381146102c55780639890220b146102eb578063cda21dee146102f3578063fdacd603146103175761009d565b806213eb4b146100a2578063091b05f6146100dc57806326bde5aa1461011c5780634a43570314610144578063654eebcb14610172575b600080fd5b6100c8600480360360208110156100b857600080fd5b50356001600160a01b0316610343565b604080519115158252519081900360200190f35b6100e4610364565b6040518082608080838360005b838110156101095781810151838201526020016100f1565b5050505090500191505060405180910390f35b6101426004803603602081101561013257600080fd5b50356001600160a01b03166103b8565b005b6101426004803603604081101561015a57600080fd5b506001600160a01b0381358116916020013516610489565b6101426004803603602081101561018857600080fd5b50356001600160a01b0316610528565b6100c8600480360360408110156101ae57600080fd5b8101906020810181356401000000008111156101c957600080fd5b8201836020820111156101db57600080fd5b803590602001918460018302840111640100000000831117156101fd57600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600092019190915250929594936020810193503591505064010000000081111561025057600080fd5b82018360208201111561026257600080fd5b8035906020019184600183028401116401000000008311171561028457600080fd5b91908080601f0160208091040260200160405190810160405280939291908181526020018383808284376000920191909152509295506105cf945050505050565b610142600480360360208110156102db57600080fd5b50356001600160a01b03166106c5565b6101426106e6565b6102fb610854565b604080516001600160a01b039092168252519081900360200190f35b6101426004803603604081101561032d57600080fd5b50803590602001356001600160a01b0316610863565b6001600160a01b03811660009081526020819052604090205415155b919050565b61036c610b64565b6000610376610a4f565b6001600160a01b031660008181526020818152604080832080548752600481015487840152600581015491870191909152928252526006015460608301525090565b6103ca816001600160a01b0316610a53565b61040c576040805162461bcd60e51b815260206004820152600e60248201526d1b9bdd08184818dbdb9d1c9858dd60921b604482015290519081900360640190fd5b610414610a59565b1561045d576040805162461bcd60e51b8152602060048201526014602482015273546f6b656e2069732073657420616c726561647960601b604482015290519081900360640190fd5b600480546001600160a01b039092166001600160a01b0319928316811790915560038054909216179055565b61049282610343565b156104d2576040805162461bcd60e51b815260206004820152600b60248201526a6e6f7420776f726b696e6760a81b604482015290519081900360640190fd5b6104db81610343565b61051a576040805162461bcd60e51b815260206004820152600b60248201526a6e6f7420776f726b696e6760a81b604482015290519081900360640190fd5b6105248282610a6a565b5050565b6000610532610a4f565b905061053d81610343565b1561057d576040805162461bcd60e51b815260206004820152600b60248201526a6e6f7420776f726b696e6760a81b604482015290519081900360640190fd5b61058682610343565b6105c5576040805162461bcd60e51b815260206004820152600b60248201526a6e6f7420776f726b696e6760a81b604482015290519081900360640190fd5b6105248183610a6a565b6000816040516020018082805190602001908083835b602083106106045780518252601f1990920191602091820191016105e5565b6001836020036101000a03801982511681845116808217855250505050505090500191505060405160208183030381529060405280519060200120836040516020018082805190602001908083835b602083106106725780518252601f199092019160209182019101610653565b6001836020036101000a0380198251168184511680821785525050505050509050019150506040516020818303038152906040528051906020012014156106bb575060016106bf565b5060005b92915050565b6106e38173a614f803b6fd780986a42c78ec9c7f77e6ded13c610a6a565b50565b60006106f0610a4f565b90506106fb81610343565b610739576040805162461bcd60e51b815260206004820152600a6024820152693737ba1032bc34b9ba1760b11b604482015290519081900360640190fd5b6000806000610746610a4f565b6001600160a01b03166001600160a01b0316815260200190815260200160002060060154905060008111801561077f575061077f610a59565b15610524576004546000906001600160a01b031663a9059cbb6107a0610a4f565b846040518363ffffffff1660e01b815260040180836001600160a01b03166001600160a01b0316815260200182815260200192505050602060405180830381600087803b1580156107f057600080fd5b505af1158015610804573d6000803e3d6000fd5b505050506040513d602081101561081a57600080fd5b50519050801561084f576000806000610831610a4f565b6001600160a01b031681526020810191909152604001600020600601555b505050565b6003546001600160a01b031690565b61086b610a59565b6108bc576040805162461bcd60e51b815260206004820152601c60248201527f506c656173652073657420617373657420746f6b656e20666972737400000000604482015290519081900360640190fd5b6004546000906001600160a01b031663dd62ed3e6108d8610a4f565b604080516001600160e01b031960e085901b1681526001600160a01b039092166004830152306024830152516044808301926020929190829003018186803b15801561092357600080fd5b505afa158015610937573d6000803e3d6000fd5b505050506040513d602081101561094d57600080fd5b50519050828110156109a6576040805162461bcd60e51b815260206004820152601960248201527f436865636b2074686520746f6b656e20616c6c6f77616e636500000000000000604482015290519081900360640190fd5b6004546001600160a01b03166323b872dd6109bf610a4f565b604080516001600160e01b031960e085901b1681526001600160a01b039092166004830152306024830152604482018790525160648083019260209291908290030181600087803b158015610a1357600080fd5b505af1158015610a27573d6000803e3d6000fd5b505050506040513d6020811015610a3d57600080fd5b50610a49905082610343565b50505050565b3390565b3b151590565b6003546001600160a01b0316151590565b6001600160a01b03808316600081815260208181526040808320948616808452818420600280546001908101808355895580890180546001600160a01b03199081168a17909155828a0180548216909517909455815487528086529386208054909316909617909155935460038501805492830181558085529290932001919091555460048201819055610afd90610b08565b600590910155505050565b60008160011415610b1b5750600161035f565b8160021415610b2c5750600261035f565b8160031415610b3d5750600361035f565b60048210158015610b4f5750600a8211155b15610b5c5750600461035f565b50600561035f565b6040518060800160405280600490602082028038833950919291505056fea265627a7a72315820c8517aa3fbee6b53c734cc183560fb7c0e78ce2be8fd16381a00ad8dc7fccc5e64736f6c634300050f0032";
public static contractName = "Network";
    __debug:boolean = true;

    tronweb: TronWeb = null;
    contract: Contract;
    contract_address_t: string;
    based_version: string = version;

    constructor(tron: TronWeb) {
        super();
        this.tronweb = tron
    }

    public static Instance(): (Network | any | boolean) {
        if (window && window.hasOwnProperty("___contract__Network__")) {
          // @ts-ignore
          const obj = window.___contract__Network__
          if (obj instanceof Network) {
            return (obj) as Network
          } else {
            return (obj) as Network
          }
        } else {
          return false
        }
    }

    async init(contract_address: string) {
        this.contract = await new Contract(this.tronweb, Network.ABI(), contract_address);
        /**this.contract = await this.tronweb.contract().new({
            abi:CONTRACT_ABI,
            bytecode: Network.deployedBytecode
        });**/
        this.contract_address_t = contract_address;
        if (window && !window.hasOwnProperty("___contract__Network__")) {
            // @ts-ignore
            window.___contract__Network__ = this
        }   
    }

    setDebug(bool:boolean){
        this.__debug = bool
    }

    public isVersionCompatible():boolean {
      return this.based_version === this.tronweb.version
    }


    // @ts-ignore
    public async commission(amount: string, ticket_buyer: string):Promise<void>{
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse:true,
            _isConstant:  false ,
            callValue:  0 ,
        }
        let val = await this.contract.commission(amount, ticket_buyer)
         .send(callparams) 
        ;

        if(this.__debug){
            console.group("==> debug return raw 💮 commission");
            console.log(val);
            console.groupEnd();
        }
        return val
    }


    // @ts-ignore
    public async compareStr(src: string, src_compared: string):Promise<boolean>{
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse:true,
            _isConstant:  true ,
            callValue:  0 ,
        }
        let val = await this.contract.compareStr(src, src_compared)
         .call(callparams) 
        ;

        if(this.__debug){
            console.group("==> debug return raw 💮 compareStr");
            console.log(val);
            console.groupEnd();
        }
        return val
    }


    // @ts-ignore
    public async drain():Promise<void>{
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse:true,
            _isConstant:  false ,
            callValue:  0 ,
        }
        let val = await this.contract.drain()
         .send(callparams) 
        ;

        if(this.__debug){
            console.group("==> debug return raw 💮 drain");
            console.log(val);
            console.groupEnd();
        }
        return val
    }


    // @ts-ignore
    public async genesisRegistration(me: string):Promise<void>{
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse:true,
            _isConstant:  false ,
            callValue:  0 ,
        }
        let val = await this.contract.genesisRegistration(me)
         .send(callparams) 
        ;

        if(this.__debug){
            console.group("==> debug return raw 💮 genesisRegistration");
            console.log(val);
            console.groupEnd();
        }
        return val
    }


    // @ts-ignore
    public async getMyDat():Promise<BigNumber[]>{
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse:true,
            _isConstant:  true ,
            callValue:  0 ,
        }
        let val = await this.contract.getMyDat()
         .call(callparams) 
        ;

        if(this.__debug){
            console.group("==> debug return raw 💮 getMyDat");
            console.log(val);
            console.groupEnd();
        }
        return val
    }


    // @ts-ignore
    public async isExist(check: string):Promise<boolean>{
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse:true,
            _isConstant:  true ,
            callValue:  0 ,
        }
        let val = await this.contract.isExist(check)
         .call(callparams) 
        ;

        if(this.__debug){
            console.group("==> debug return raw 💮 isExist");
            console.log(val);
            console.groupEnd();
        }
        return val
    }


    // @ts-ignore
    public async registerFast(upperline: string):Promise<void>{
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse:true,
            _isConstant:  false ,
            callValue:  0 ,
        }
        let val = await this.contract.registerFast(upperline)
         .send(callparams) 
        ;

        if(this.__debug){
            console.group("==> debug return raw 💮 registerFast");
            console.log(val);
            console.groupEnd();
        }
        return val
    }


    // @ts-ignore
    public async registerName(me: string, upperline: string):Promise<void>{
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse:true,
            _isConstant:  false ,
            callValue:  0 ,
        }
        let val = await this.contract.registerName(me, upperline)
         .send(callparams) 
        ;

        if(this.__debug){
            console.group("==> debug return raw 💮 registerName");
            console.log(val);
            console.groupEnd();
        }
        return val
    }


    // @ts-ignore
    public async seeTokenAddress():Promise<string>{
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse:true,
            _isConstant:  true ,
            callValue:  0 ,
        }
        let val = await this.contract.seeTokenAddress()
         .call(callparams) 
        ;

        if(this.__debug){
            console.group("==> debug return raw 💮 seeTokenAddress");
            console.log(val);
            console.groupEnd();
        }
        return val
    }


    // @ts-ignore
    public async setAssetToken(address_loc: string):Promise<void>{
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse:true,
            _isConstant:  false ,
            callValue:  0 ,
        }
        let val = await this.contract.setAssetToken(address_loc)
         .send(callparams) 
        ;

        if(this.__debug){
            console.group("==> debug return raw 💮 setAssetToken");
            console.log(val);
            console.groupEnd();
        }
        return val
    }

   /**
     * @returns The contract ABI
     */
    public static ABI(): any {
        const abi = [
            { 
                constant: false,
                inputs: [
                    {
                        name: 'amount',
                        type: 'uint256',
                    },
                    {
                        name: 'ticket_buyer',
                        type: 'address',
                    },
                ],
                name: 'commission',
                outputs: [
                ],
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
                inputs: [
                ],
                name: 'drain',
                outputs: [
                ],
                payable: false,
                stateMutability: 'nonpayable',
                type: 'function',
            },
            { 
                constant: false,
                inputs: [
                    {
                        name: 'me',
                        type: 'address',
                    },
                ],
                name: 'genesisRegistration',
                outputs: [
                ],
                payable: false,
                stateMutability: 'nonpayable',
                type: 'function',
            },
            { 
                constant: true,
                inputs: [
                ],
                name: 'getMyDat',
                outputs: [
                    {
                        name: 'mdat',
                        type: 'uint256[4]',
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
                        name: 'check',
                        type: 'address',
                    },
                ],
                name: 'isExist',
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
                inputs: [
                    {
                        name: 'upperline',
                        type: 'address',
                    },
                ],
                name: 'registerFast',
                outputs: [
                ],
                payable: false,
                stateMutability: 'nonpayable',
                type: 'function',
            },
            { 
                constant: false,
                inputs: [
                    {
                        name: 'me',
                        type: 'address',
                    },
                    {
                        name: 'upperline',
                        type: 'address',
                    },
                ],
                name: 'registerName',
                outputs: [
                ],
                payable: false,
                stateMutability: 'nonpayable',
                type: 'function',
            },
            { 
                constant: true,
                inputs: [
                ],
                name: 'seeTokenAddress',
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
                        name: 'address_loc',
                        type: 'address',
                    },
                ],
                name: 'setAssetToken',
                outputs: [
                ],
                payable: false,
                stateMutability: 'nonpayable',
                type: 'function',
            },
        ];
        return abi;
    }
}