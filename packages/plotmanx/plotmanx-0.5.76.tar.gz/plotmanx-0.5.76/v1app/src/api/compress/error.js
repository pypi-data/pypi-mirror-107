function error_explain(error_code) {
  const error_map = {
    USER_NOT_EXIST: 2,
    USER_ALREADY_EXIST: 3,
    INVALID_AMOUNT: 4,
    NOT_USER_ADDRESS: 5,
    INVALID_DONOR: 6,
    SNAPTIME_IS_OVER: 7,
    INVALID_MATRIX: 8,
    INVALID_LEVEL: 9,
    LEVEL_ALREADY_ACTIVATED: 10,
    REFERRER_NOT_EXIST: 11,
    REFERRER_LEVEL_INACTIVE: 12,
    CANNOT_BE_SMART_CONTRACT: 13,
    CONTRACT_IS_FINALIZED: 14,
    REFERCODE_NOT_EXIST: 15,
    INVITECODE_EXIST: 16
  }
  console.log("got error from ", error_code)
  const codemsg = _.findKey(error_map, function (o) {
    return o === error_code
  })
  if (error_code === 0) {
    return ""
  }

  if (codemsg === undefined) {
    return "unknown error"
  } else {
    return codemsg
  }
}

export {
  error_explain
}
