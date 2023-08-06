import { EventBus } from "vue-backgrounds"

/**
 * query the referral code from the url bar
 */
function getURLReferralCode() {
  const uri = window.location.search.substring(1)
  const params = new URLSearchParams(uri)
  if (params.has("code")) {
    const code_test = params.get("code")
    EventBus.$emit("bottom_sheet_refer", code_test)
  }
}

function getStoredItemInt(key, _default) {
  if (localStorage) {
    if (localStorage.getItem(key) === null) {
      return _default
    } else {
      return parseInt(localStorage.getItem(key))
    }
  } else {
    return _default
  }
}

function getStoredItemStr(key, _default_str) {
  if (localStorage) {
    if (localStorage.getItem(key) === null) {
      return _default_str
    } else {
      return parseInt(localStorage.getItem(key))
    }
  } else {
    return _default_str
  }
}

export {
  getURLReferralCode,
  getStoredItemInt,
  getStoredItemStr
}
