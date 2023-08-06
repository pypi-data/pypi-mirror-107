<template>
  <v-flex :class="`cardplan ${status}`" xs12 sm6 md3 s>
    <Varsace name-tag="gold"/>
    <h1 class="level_title">Chapter {{ title }}</h1>
    <h3>
      <sup>{{ currency }}</sup>{{ amount | coinbalance }}
      <span v-if="per.length>0" class="small">/{{ per }}</span>
    </h3>
    <v-btn
      v-if="sale"
      x-large
      ripple
      dark
      bottom
      elevation="19"
      class="enter_deal_button"
      @click="enter_deal">
      {{ buttonLabel }}
    </v-btn>
    <v-card v-if="!sale" elevation="5">
      <v-card-title>Fulfilled 3</v-card-title>
    </v-card>
    <!-- </v-card>-->
  </v-flex>
</template>
<script>
import { EventBus } from "vue-backgrounds"

export default {
  name: "VCardPriceplan",

  props: {
    title: {
      type: String,
      required: true
    },
    currency: {
      type: String,
      required: false,
      default: "$"
    },
    amount: {
      type: String,
      required: false,
      default: "000"
    },
    per: {
      type: String,
      required: false,
      default: ""
    },
    specialDealDescription: {
      type: String,
      required: false,
      default: "000"
    },
    sale: {
      type: Boolean,
      required: false,
      default: false
    },
    buttonLabel: {
      type: String,
      required: false,
      default: "Sign Up"
    }
  },
  data() {
    return {
      status: this.sale ? "empty" : ""
    }
  },
  methods: {
    enter_deal(e) {
      e.preventDefault()
      EventBus.$emit("price_plan_enter_deal", this.key, this.amount)
    }
  }
}
</script>
