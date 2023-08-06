import _ from "lodash"
import web3 from "web3"
function genPrizeRule() {
  const ruleSet = []
  ruleSet[0] = [40, 270, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  ruleSet[1] = [0, 180, 509, 0, 0, 0, 0, 0, 0, 0, 0]
  ruleSet[2] = [0, 0, 280, 5000, 0, 0, 0, 0, 0, 0, 0]
  ruleSet[3] = [0, 0, 170, 1000, 10000, 0, 0, 0, 0, 0, 0]
  ruleSet[4] = [0, 0, 140, 400, 1400, 39000, 0, 0, 0, 0, 0]
  ruleSet[5] = [0, 0, 0, 300, 900, 18000, 71000, 0, 0, 0, 0]
  ruleSet[6] = [0, 0, 0, 200, 700, 3000, 40000, 80000, 0, 0, 0]
  ruleSet[7] = [0, 0, 0, 200, 400, 1100, 6700, 40000, 90000, 0, 0]
  ruleSet[8] = [0, 0, 0, 200, 250, 500, 1500, 10000, 50000, 100000, 0]
  ruleSet[9] = [0, 0, 0, 160, 200, 400, 700, 2600, 10000, 50000, 100000]
  return ruleSet
}

function hit(picks) {
  const f = genPrizeRule()
  if (picks > 0) {
    const g = f[picks - 1].map((x) => {
      const txt = x / 100
      return `${txt}x`
    })
    return g.slice(0, picks + 1)
  } else {
    return []
  }
}

function matchprize(bet, history, declare_prize_at_round) {
  let hits = 0
  const f = genPrizeRule()
  _.forEach(history, (a, b, c) => {
    if (a.includes(declare_prize_at_round)) {
      hits++
    }
  })
  const x = f[history.length][hits]
  return {
    bet,
    x,
    returns: bet * x,
    label: `${x}X`
  }
}

function generateHashDraw() {
  return web3.utils.randomHex(32)
}

export {
  hit,
  matchprize,
  generateHashDraw
}
