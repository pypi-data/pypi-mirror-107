<template>
  <div class="ticket_boxes card-group">
    <div v-for="(ibox,n) in list_tickets" :key="n" :class="checkCardStatus(ibox.kjid)" class="card-h">
      <div class="rightbox">
        <button :data-gm="n" class="btn roundc shapedup" @click="followUp">
          追號🎟
        </button>
        <button :data-tid="ibox.transid" class="btn roundc shapedup" @click="checkUp">
          查證🔍
        </button>
      </div>
      <article>🎟票號: {{ ibox.transid }}</article>
      <article>🌠开奖期號: {{ ibox.kjid }}</article>
      <article>🏖博弈规则: {{ ibox.rules[0] }} <a>📜 游戏描述 </a></article>
      <div v-if="ibox.rules[0].split('-')[0]==='star'" class="ticket-1">
        <ul v-show="ibox.g1.length>0">
          <li>個位</li>
          <li v-for="(tn,u) in ibox.g1" :key="u">{{ tn }}</li>
        </ul>
        <ul v-show="ibox.g2.length>0">
          <li>十位</li>
          <li v-for="(tn,y) in ibox.g2" :key="y">{{ tn }}</li>
        </ul>
        <ul v-show="ibox.g3.length>0">
          <li>百位</li>
          <li v-for="(tn,r) in ibox.g3" :key="r">{{ tn }}</li>
        </ul>
        <ul v-show="ibox.g4.length>0">
          <li>千位</li>
          <li v-for="(tn,o) in ibox.g4" :key="o">{{ tn }}</li>
        </ul>
        <ul v-show="ibox.g5.length>0">
          <li>万位</li>
          <li v-for="(tn,w) in ibox.g5" :key="w">{{ tn }}</li>
        </ul>
      </div>

      <div v-if="ibox.rules[0]==='simple-a'" class="ticket-2">
        <ul v-show="ibox.g1.length>0">
          <li>投</li>
          <li>{{ ibox.g1[0] }}</li>
        </ul>
      </div>

      <p>${{ ibox.base }}每注, {{ ibox.factor }} x倍, {{ ibox.bets }}x注, ${{ ibox.amount |fix3 }}</p>
    </div>
    <div class="bottom_bar">
      <span class="close_button" @click="$emit('close_x')">
        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 130.2 130.2">
          <circle class="path circle" fill="#EDEDED" stroke="#D06079" stroke-width="6" stroke-miterlimit="10"
                  cx="65.1"
                  cy="65.1"
                  r="62.1"/>
          <line class="path line" fill="none" stroke="#D06079" stroke-width="6" stroke-linecap="round"
                stroke-miterlimit="10"
                x1="34.4" y1="37.9" x2="95.8" y2="92.3"/>
          <line class="path line" fill="none" stroke="#D06079" stroke-width="6" stroke-linecap="round"
                stroke-miterlimit="10"
                x1="95.8" y1="38" x2="34.4" y2="92.2"/>
        </svg>
      </span>
    </div>
  </div>
</template>

<script>

import { EventBus } from "vue-backgrounds"

export default {
  name: "ScoreCard",
  computed: {
    list_tickets: {
      get () {
        return this.$store.state.kaijiang.tickets
      }
    },
    notification_num: {
      get () {
        return this.$store.state.kaijiang.tickets.length
      }
    },
    lastKJ: {
      get () {
        return this.$store.state.kaijiang.kj_period_n
      }
    }
  },
  methods: {
    followUp (e) {
      const ticket = this.list_tickets[parseInt(e.target.dataset.gm)]
      this.$emit("followBet", ticket)
      EventBus.$emit("followBet", ticket)
    },
    checkUp (e) {
      const transaction_id = e.target.dataset.tid
      EventBus.$emit("check_result_transaction_id", transaction_id)
    },
    checkCardStatus (jkId) {
      const ticket_jkid = parseInt(jkId)
      if (ticket_jkid > this.lastKJ) {
        return "coming"
      } else {
        return "passevent"
      }
    }
  }

}
</script>

<style lang="scss" scoped>
    @mixin luckyball {
        color: #000000;
        background: linear-gradient(#e5e110, #d28b11);
        border-color: #9c1308;
        border-width: 2px;
        box-shadow: 0 2px 3px 0px rgba(0, 0, 0, 0.25);
        font-weight: 400;
        border-radius: 49%;
        line-height: 16px;

        text-align: center;
        padding-left: 5px;
        padding-right: 5px;
        margin-right: 4px;
        -webkit-font-smoothing: subpixel-antialiased;
    }

    @mixin tag {
        margin: 1px;
        list-style: none;
        display: inline-block;
        flex-wrap: nowrap;
        box-shadow: 0 2px 3px 0px rgba(0, 0, 0, 0.25);
        background: linear-gradient(#18e50d, #136010);
        color: #f5e6a2;
        border-radius: 2px;
    }

    @mixin luckyaction {
        color: #000000;
        background: linear-gradient(#e5e110, #d28b11);
        border-color: #9c1308;
        border-width: 2px;
        box-shadow: 0 2px 3px 0px rgba(0, 0, 0, 0.25);
        font-weight: 400;
        border-radius: 1px;
        line-height: 16px;
        text-align: center;
        padding-left: 5px;
        padding-right: 5px;
        margin-right: 4px;
    }

    @mixin goldcard {
        background: radial-gradient(ellipse farthest-corner at right bottom, #FEDB37 0%, #FDB931 8%, #9f7928 30%, #8A6E2F 40%, transparent 80%),
        radial-gradient(ellipse farthest-corner at left top, #FFFFFF 0%, #FFFFAC 8%, #D1B464 25%, #5d4a1f 62.5%, #5d4a1f 100%);
    }

    .rightbox {
        position: absolute;
        display: flex;
        //z-index: 1;
        right: 2px;
        width: 120px;
        .shapedup {
            flex: 1;
            height: auto;
            flex-wrap: nowrap;
            background: linear-gradient(#c3a947, #9c7707);
        }
        button {
            margin: 0
        }

    }

    .ticket_boxes {
        display: flex;
        height: 100vh;
        width: 100%;
        flex-direction: column;
        background: #3e2704;
        overflow: scroll;
        padding-bottom: 100px;
        div {
            font-size: 0.03em;
            color: #544216;
        }

        .card-h {
            border-radius: 5px;
            margin: 2px;
            padding-top: 3px;
            padding-bottom: 3px;
            padding-left: 8px;
            position: relative;

            &.passevent {
                background: #040401;
                &.win {
                    @include goldcard;
                    color: black;
                }
            }

            &.coming {
                background: #f5e6a2;
            }
            .ticket-1 {
                ul {
                    padding: 3px;
                    display: flex;
                    font-size: 8px;
                    li {
                        margin: 1px;
                        list-style: none;
                        display: inline-block;
                        flex-wrap: nowrap;
                        @include luckyball;
                    }
                    li:first-child {
                        @include tag;
                    }
                }
            }
            .ticket-2 {
                ul {
                    padding: 3px;
                    display: flex;
                    font-size: 8px;
                    li {
                        margin: 1px;
                        list-style: none;
                        display: inline-block;
                        flex-wrap: nowrap;
                        @include luckyaction;
                    }
                    li:first-child {
                        @include tag;
                    }
                }
            }

        }
        .bottom_bar {
            background: linear-gradient(#c3a947, #9c7707);
            position: fixed;
            bottom: 0;
            height: 40px;
            width: 100%;
            text-align: center;
            span {
                text-align: center;
            }
            z-index: 1;
        }
    }

</style>
