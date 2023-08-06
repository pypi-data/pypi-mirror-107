<template>
  <div class="cgrid">
    <filter-bar/>
    <vuetable
      ref="vuetable"
      :api-mode="false"
      :fields="fields"
      :per-page="10"
      :multi-sort="true"
      :sort-order="sortOrder"
      :append-params="appendParams"
      :detail-row-component="detailRowComponent"
      :data="data"
      :row-class="state_valid"
      pagination-path=""
      @cell-clicked="onCellClicked"
      @pagination-data="onPaginationData"
    />
    <vuetable-pagination
      class="vuetable-pagination ui basic segment grid">
      <vuetable-pagination-info ref="paginationInfo"/>
      <vuetable-pagination ref="pagination"
                           @change-page="onChangePage"/>
    </vuetable-pagination>
  </div>
</template>
<style lang="scss">
  .cgrid {
    color: white;
    width: 100%;
    .vuetable {
      width: 100%;
    }
    .filter-bar {
      width: 100%;
    }
    .vuetable-body {
      tr {
        color: #bbc3fa;
        background-color: #0DFF92;
        &.invalid {
          color: #f03d00;
          background-color: #a82c29;
        }
        &.valid {
          color: #faebf6;
          background-color: #0DFF92;
        }
        .actionbar{
          background-color: #9ad5ac;
        }
      }
    }
  }
</style>
<script>
// import accounting from "accounting"
// import moment from "moment"
// import Vue from "vue"
// import VueEvents from "vue-events"
import Vuetable from "vuetable-2/src/components/Vuetable"
import VuetablePagination from "vuetable-2/src/components/VuetablePagination"
import VuetablePaginationInfo from "vuetable-2/src/components/VuetablePaginationInfo"
import CustomActions from "./CustomActions"
import FilterBar from "./FilterBar"

function countDecimals (h) {
  const value = parseFloat(h)
  if (Math.floor(value) !== value) { return value.toString().split(".")[1].length || 0 }
  return 0
}

export default {
  components: {
    Vuetable,
    VuetablePagination,
    VuetablePaginationInfo,
    CustomActions,
    FilterBar
  },
  props: {
    /*  apiUrl : {
          type : String,
          required : false
        }, */
    data: {
      type: Array,
      default () {
        return []
      }
    },
    fields: {
      type: Array,
      required: true
    },
    sortOrder: {
      type: Array,
      default () {
        return []
      }
    },
    appendParams: {
      type: Object,
      default () {
        return {}
      }
    },
    detailRowComponent: {
      type: String,
      default () {
        return ""
      }
    },
    decimal: {
      type: Number,
      default () {
        return 18
      }
    }
  },
  data () {
    return {}
  },
  computed: {},
  mounted () {
    this.$on("filter-set", e => this.onFilterSet(e))
    this.$on("filter-reset", () => this.onFilterReset())
  },
  methods: {
    state_valid (dataItem) {
      const c = this.$store.getters["mulsend/get_dec"]
      if (c >= countDecimals(dataItem.cost)) {
        return "valid-ok"
      } else {
        return "invalid"
      }
    },
    /*
       onRowClass(dataItem, index) {
        return this.$refs.vuetable.selectedTo.includes(dataItem.id)
           ? 'bg-blu'
           : 'bg-white'

       }, */
    // render related functions
    /* renderVuetable (h) {
         return h (
           "vuetable",
           {
             ref : "vuetable",
             props : {
               apiUrl : this.apiUrl,
               fields : this.fields,
               paginationPath : "",
               perPage : 10,
               multiSort : true,
               sortOrder : this.sortOrder,
               appendParams : this.appendParams,
               detailRowComponent : this.detailRowComponent,
             },
             on : {
               "vuetable:cell-clicked" : this.onCellClicked,
               "vuetable:pagination-data" : this.onPaginationData,
             },
             scopedSlots : this.$vnode.data.scopedSlots
           }
         )
       }, */
    /*   renderPagination (h) {
           return h (
             "div",
             { class : { "vuetable-pagination" : true, "ui" : true, "basic" : true, "segment" : true, "grid" : true } },
             [
               h ("vuetable-pagination-info", { ref : "paginationInfo" }),
               h ("vuetable-pagination", {
                 ref : "pagination",
                 on : {
                   "vuetable-pagination:change-page" : this.onChangePage
                 }
               })
             ]
           )
         }, */

    // ------------------
    refresh () {
      // console.log("refresh data");
      this.$refs.vuetable.refresh()
    },
    /* allcap (value) {
         return value.toUpperCase ()
       },
       genderLabel (value) {
         return value === "M"
           ? `<span class="ui teal label"><i class="large man icon"></i>Male</span>`
           : `<span class="ui pink label"><i class="large woman icon"></i>Female</span>`
       },
       formatNumber (value) {
         return accounting.formatNumber (value, 2)
       },
       formatDate (value, fmt = "D MMM YYYY") {
         return (value == null)
           ? ""
           : moment (value, "YYYY-MM-DD").format (fmt)
       }, */
    onPaginationData (paginationData) {
      this.$refs.pagination.setPaginationData(paginationData)
      this.$refs.paginationInfo.setPaginationData(paginationData)
    },
    onChangePage (page) {
      this.$refs.vuetable.changePage(page)
    },
    onCellClicked (data, field) {
      console.log("cellClicked: ", field.address)
      this.$refs.vuetable.toggleDetailRow(data.id)
    },
    onFilterSet (filterText) {
      this.appendParams.filter = filterText
      this.$nextTick(() => this.$refs.vuetable.refresh())
    },
    onFilterReset () {
      delete this.appendParams.filter
      this.$nextTick(() => this.$refs.vuetable.refresh())
    }
  }
}
</script>
