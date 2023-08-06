const SOURCE = Object.freeze({
  zh: require("./lang/_zh.json"), // 中文语言包
  in: require("./lang/_in.json"), // Indian语言包
  ko: require("./lang/_kr.json"), // Ko语言包
  th: require("./lang/_th.json"), // Thai语言包
  jp: require("./lang/_jp.json"), // Japan语言包
  en: require("./lang/_en.json") // 英文语言包
})
const DETAILS = Object.freeze([
  {
    source: require("./lang/_en.json"),
    key: "en",
    label: "🇺🇸 English"
  },
  {
    source: require("./lang/_zh.json"),
    key: "zh",
    label: "🇨🇳 中文语言包"
  },
  {
    source: require("./lang/_kr.json"),
    key: "ko",
    label: "🇰🇷 한국어"
  },
  {
    source: require("./lang/_th.json"),
    key: "th",
    label: "🇹🇭 ภาษาไทย"
  },
  {
    source: require("./lang/_jp.json"),
    key: "jp",
    label: "🇯🇵 日本語"
  },
  {
    source: require("./lang/_in.json"),
    key: "in",
    label: "🇮🇳 भारतीय"
  }
])
const LIST = Object.keys(SOURCE)

export const LANUAGES = Object.freeze({
  SOURCE,
  DETAILS,
  LIST
})

export const LANUAGESMIX = {
  created() {
    this.languages = DETAILS
  }
}
