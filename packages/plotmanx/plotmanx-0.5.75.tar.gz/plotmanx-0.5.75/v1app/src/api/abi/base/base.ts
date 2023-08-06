// @ts-ignore
import tron from "tronweb"
import { EventEmitter } from "eventemitter3"
import { ReqEventResult } from "abi/base/types"

export default class BaseContract extends EventEmitter {
  protected decodeValues(params: any): Array<any> {
    let results = []
    // @ts-ignore
    if (tron.utils.isArray(params)) {
      const l = params.length
      for (let h = 0; h < l; h++) {
        // @ts-ignore
        if (tron.utils.isBigNumber(params[h])) {
          // @ts-ignore
          results.push(params[h].toString())
        } else {
          console.log("parse outside :: ", params[h])
        }
      }
    } else {
      results = []
    }
    return results
  }

  public sortEventsAscending(list: Array<ReqEventResult>): Array<ReqEventResult> {
    if (list.length > 2) {
      return list.sort(function (a, b) {
        return a.block - b.block
      })
    } else {
      return list
    }
  }

  public sortEventsDescending(list: Array<ReqEventResult>): Array<ReqEventResult> {
    if (list.length > 2) {
      return list.sort(function (a, b) {
        return b.block - a.block
      })
    } else {
      return list
    }
  }
}
