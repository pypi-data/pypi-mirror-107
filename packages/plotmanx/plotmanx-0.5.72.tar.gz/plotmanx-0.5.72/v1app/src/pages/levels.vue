<template>
  <section id="indexbox" class="indexcolor">
    <div class="backee home">
    </div>
    <v-main class="price-plan-layout">
      <v-container class="container group">
        <v-layout row wrap fill-height>
          <v-card-priceplan
            v-for="(cell, index) in cells"
            :key="cell.key"
            :ref="`${TYPESC.BASE_REF_NAME}${index}`"
            :per="precontent"
            :currency="cell.currency"
            :amount="cell.amount"
            :title="cell.title"
            :sale="cell.blocked_x3"
            :button-label="$t('bnt_deal')"
            class="planbox"
          />
        </v-layout>
      </v-container>
    </v-main>
  </section>
</template>
<script>

// eslint-disable-next-line no-unused-vars
import { TYPESCMIX, TYPESC } from "vue-codepin/src/components/priceplan/const"
import VCardPriceplan from "@/components/priceplan/plan"
import price_plan from "@/api/mixins/tron/price_plan"
import { EventBus } from "vue-backgrounds"

export default {
  name: "Priceplan",
  components: { VCardPriceplan },
  layout: "bottom",
  mixins: [TYPESCMIX, price_plan],
  data() {
    return {
      precontent: "Lot",
      watchers: {},
      cellsInputTypes: {}
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.LanguageStart()
      this.setup_levels()
      this.update_price_plan()
      this.check_lvl_plan()
      EventBus.$on("check_price_plan_action", this.check_price_plan_action)
    })
  },
  beforeDestroy() {
    EventBus.$off("check_price_plan_action", this.check_price_plan_action)
  },
  methods: {
    check_price_plan_action() {
      this.update_price_plan()
      this.check_lvl_plan()
    }
  }
}
</script>
