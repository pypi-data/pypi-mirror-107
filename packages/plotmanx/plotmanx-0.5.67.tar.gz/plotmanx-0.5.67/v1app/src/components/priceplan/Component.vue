<template>
  <div class="price-plan-layout">
    <div class="container group">
      <plan
        v-for="(cell, index) in cells"
        :key="cell.key"
        :ref="`${TYPESC.BASE_REF_NAME}${index}`"
        :per="precontent"
        :currency="cell.currency"
        :amount="cell.amount"
        :title="cell.title"
        :button-label="button_label"
        class="planbox"
        @price_plan_enter_deal="$event"
      />
    </div>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars

import Plan from "./plan.vue"
// eslint-disable-next-line no-unused-vars
import { TYPESCMIX, TYPESC } from "./const"
// I, II, III, IV, V, VI, VII, VIII, IX, X, XI, XII
export default {
  name: "PricePlan",
  components: { Plan },
  mixins: [TYPESCMIX],
  data() {
    return {
      button_label: "Activate!",
      precontent: "Addr",
      watchers: {},
      cellsInputTypes: {},
      cells: []
    }
  }
}
</script>
