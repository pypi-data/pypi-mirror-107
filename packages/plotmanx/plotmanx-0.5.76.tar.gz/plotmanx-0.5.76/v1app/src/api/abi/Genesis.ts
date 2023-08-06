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
    compareStr(src: string, src_compared: string):Promise<boolean>
    dist(amount: string):Promise<void>
    seeTokenAddress():Promise<string>
    setAssetToken(address_loc: string):Promise<void>
}

// @ts-ignore
export class Genesis extends BaseContract implements ContractInterface {

public static deployedBytecode = "60806040526000805473a5576e55542477ce999f2d3a8c242697b0fcf4166001600160a01b03199182168117909255600180548216831790556002805482168317905560038054909116909117905561090e8061005d6000396000f3fe608060405234801561001057600080fd5b506004361061004c5760003560e01c806326bde5aa1461005157806387c5d5cc14610079578063bc5c0fcc146101ba578063cda21dee146101d7575b600080fd5b6100776004803603602081101561006757600080fd5b50356001600160a01b03166101fb565b005b6101a66004803603604081101561008f57600080fd5b8101906020810181356401000000008111156100aa57600080fd5b8201836020820111156100bc57600080fd5b803590602001918460018302840111640100000000831117156100de57600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600092019190915250929594936020810193503591505064010000000081111561013157600080fd5b82018360208201111561014357600080fd5b8035906020019184600183028401116401000000008311171561016557600080fd5b91908080601f0160208091040260200160405190810160405280939291908181526020018383808284376000920191909152509295506102cc945050505050565b604080519115158252519081900360200190f35b610077600480360360208110156101d057600080fd5b50356103c2565b6101df610875565b604080516001600160a01b039092168252519081900360200190f35b61020d816001600160a01b0316610884565b61024f576040805162461bcd60e51b815260206004820152600e60248201526d1b9bdd08184818dbdb9d1c9858dd60921b604482015290519081900360640190fd5b61025761088a565b156102a0576040805162461bcd60e51b8152602060048201526014602482015273546f6b656e2069732073657420616c726561647960601b604482015290519081900360640190fd5b600580546001600160a01b039092166001600160a01b0319928316811790915560048054909216179055565b6000816040516020018082805190602001908083835b602083106103015780518252601f1990920191602091820191016102e2565b6001836020036101000a03801982511681845116808217855250505050505090500191505060405160208183030381529060405280519060200120836040516020018082805190602001908083835b6020831061036f5780518252601f199092019160209182019101610350565b6001836020036101000a0380198251168184511680821785525050505050509050019150506040516020818303038152906040528051906020012014156103b8575060016103bc565b5060005b92915050565b600081116104015760405162461bcd60e51b81526004018080602001828103825260258152602001806108b56025913960400191505060405180910390fd5b61040961088a565b61045a576040805162461bcd60e51b815260206004820152601c60248201527f506c656173652073657420617373657420746f6b656e20666972737400000000604482015290519081900360640190fd5b6005546000906001600160a01b031663dd62ed3e61047661089b565b604080516001600160e01b031960e085901b1681526001600160a01b039092166004830152306024830152516044808301926020929190829003018186803b1580156104c157600080fd5b505afa1580156104d5573d6000803e3d6000fd5b505050506040513d60208110156104eb57600080fd5b5051905081811015610544576040805162461bcd60e51b815260206004820152601960248201527f436865636b2074686520746f6b656e20616c6c6f77616e636500000000000000604482015290519081900360640190fd5b6005546001600160a01b03166323b872dd61055d61089b565b604080516001600160e01b031960e085901b1681526001600160a01b039092166004830152306024830152604482018690525160648083019260209291908290030181600087803b1580156105b157600080fd5b505af11580156105c5573d6000803e3d6000fd5b505050506040513d60208110156105db57600080fd5b50506005546000546001600160a01b039182169163a9059cbb911661060785600463ffffffff61089f16565b6040518363ffffffff1660e01b815260040180836001600160a01b03166001600160a01b0316815260200182815260200192505050602060405180830381600087803b15801561065657600080fd5b505af115801561066a573d6000803e3d6000fd5b505050506040513d602081101561068057600080fd5b50506005546001546001600160a01b039182169163a9059cbb91166106ac85600463ffffffff61089f16565b6040518363ffffffff1660e01b815260040180836001600160a01b03166001600160a01b0316815260200182815260200192505050602060405180830381600087803b1580156106fb57600080fd5b505af115801561070f573d6000803e3d6000fd5b505050506040513d602081101561072557600080fd5b50506005546002546001600160a01b039182169163a9059cbb911661075185600463ffffffff61089f16565b6040518363ffffffff1660e01b815260040180836001600160a01b03166001600160a01b0316815260200182815260200192505050602060405180830381600087803b1580156107a057600080fd5b505af11580156107b4573d6000803e3d6000fd5b505050506040513d60208110156107ca57600080fd5b50506005546003546001600160a01b039182169163a9059cbb91166107f685600463ffffffff61089f16565b6040518363ffffffff1660e01b815260040180836001600160a01b03166001600160a01b0316815260200182815260200192505050602060405180830381600087803b15801561084557600080fd5b505af1158015610859573d6000803e3d6000fd5b505050506040513d602081101561086f57600080fd5b50505050565b6004546001600160a01b031690565b3b151590565b6004546001600160a01b0316151590565b3390565b6000808284816108ab57fe5b0494935050505056fe596f75206e65656420746f2073656c6c206174206c6561737420736f6d6520746f6b656e73a265627a7a72315820c3bbe2569acdf871aed42a1b60131665597175e15c38747dd9bc6702cd5ae3a364736f6c634300050f0032";
public static contractName = "Genesis";
    __debug:boolean = true;

    tronweb: TronWeb = null;
    contract: Contract;
    contract_address_t: string;
    based_version: string = version;

    constructor(tron: TronWeb) {
        super();
        this.tronweb = tron
    }

    public static Instance(): (Genesis | any | boolean) {
        if (window && window.hasOwnProperty("___contract__Genesis__")) {
          // @ts-ignore
          const obj = window.___contract__Genesis__
          if (obj instanceof Genesis) {
            return (obj) as Genesis
          } else {
            return (obj) as Genesis
          }
        } else {
          return false
        }
    }

    async init(contract_address: string) {
        this.contract = await new Contract(this.tronweb, Genesis.ABI(), contract_address);
        /**this.contract = await this.tronweb.contract().new({
            abi:CONTRACT_ABI,
            bytecode: Genesis.deployedBytecode
        });**/
        this.contract_address_t = contract_address;
        if (window && !window.hasOwnProperty("___contract__Genesis__")) {
            // @ts-ignore
            window.___contract__Genesis__ = this
        }   
    }

    setDebug(bool:boolean){
        this.__debug = bool
    }

    public isVersionCompatible():boolean {
      return this.based_version === this.tronweb.version
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
    public async dist(amount: string):Promise<void>{
        let callparams = {
            userFeePercentage: 30,
            feeLimit: 100000000,
            shouldPollResponse:true,
            _isConstant:  false ,
            callValue:  0 ,
        }
        let val = await this.contract.dist(amount)
         .send(callparams) 
        ;

        if(this.__debug){
            console.group("==> debug return raw 💮 dist");
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
                    {
                        name: 'amount',
                        type: 'uint256',
                    },
                ],
                name: 'dist',
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