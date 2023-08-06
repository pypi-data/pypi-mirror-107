<template>
  <section id="indexbox" class="container indexcolor">
    <div class="backee home">

    </div>
    <div class="toplayer wgrid">

      <my-vuetable
        ref="vTable"
        :fields="fields"
        :sort-order="sortOrder"
        :append-params="moreParams"
        :data="market_data"
        detail-row-component="detail-row"
        class="row"
      >
        <template slot="actions" slot-scope="props">
          <div class="custom-actions">
            <button class="ui basic button"
                    @click="onAction('view-item', props.rowData, props.rowIndex)">
              <i class="zoom icon"></i>
            </button>
            <button class="ui basic button"
                    @click="onAction('edit-item', props.rowData, props.rowIndex)">
              <i class="edit icon"></i>
            </button>
            <button class="ui basic button"
                    @click="onAction('delete-item', props.rowData, props.rowIndex)">
              <i class="delete icon"></i>
            </button>
          </div>
        </template>
      </my-vuetable>
      <div class="row">
        <div class="col col-4-of-12 rgreybox center" @click="returnhome"><span
          class="starkl">{{ label_return_home }}</span>
        </div>
        <div class="col col-4-of-12 rgreybox center" @click="returnhome"><span class="starkl">{{ label_sales }}</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script>

import _ from "lodash"
import MyVuetable from "../components/table/MyVuetable"
import FieldDefs from "../components/table/FieldDefs.js"

export default {
  name: "Marketplace",
  components: {
    MyVuetable
  },
  data() {
    return {
      fields: FieldDefs,
      market_data: [],
      sortOrder: [
        {
          field: "cost",
          sortField: "cost",
          direction: "asc"
        }
      ],
      moreParams: {},
      label_return_home: "HOME",
      label_sales: "SELL"
    }
  },
  mounted() {
    const data = [
      {
        id: 0,
        address: "0x9320930923",
        cost: "32.0",
        nodecount: 22,
        income: "102.1"
      }, {
        id: 1,
        address: "0x9320930923",
        cost: "34.0",
        nodecount: 40,
        income: "152.1"
      }
    ]

    this.$nextTick(() => {
      _.forEach(data, (a, b, c) => {
        this.market_data.push({
          id: a.id,
          address: a.address,
          cost: a.cost,
          nodecount: a.nodecount,
          income: a.income
        })
      })

      console.log(this.market_data)
    })
  },
  methods: {
    onAction(action, data, index) {
      console.log("slot action: " + action, data.name, index)
    },
    returnhome() {
      this.$router.push("/")
    }
  }
}
</script>

<style scoped>

</style>
