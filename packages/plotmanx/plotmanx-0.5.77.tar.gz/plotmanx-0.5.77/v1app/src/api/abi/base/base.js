import tron from "tronweb";
import { EventEmitter } from "eventemitter3";
export default class BaseContract extends EventEmitter {
    decodeValues(params) {
        let results = [];
        if (tron.utils.isArray(params)) {
            const l = params.length;
            for (let h = 0; h < l; h++) {
                if (tron.utils.isBigNumber(params[h])) {
                    results.push(params[h].toString());
                }
                else {
                    console.log("parse outside :: ", params[h]);
                }
            }
        }
        else {
            results = [];
        }
        return results;
    }
    sortEventsAscending(list) {
        if (list.length > 2) {
            return list.sort(function (a, b) {
                return a.block - b.block;
            });
        }
        else {
            return list;
        }
    }
    sortEventsDescending(list) {
        if (list.length > 2) {
            return list.sort(function (a, b) {
                return b.block - a.block;
            });
        }
        else {
            return list;
        }
    }
}
