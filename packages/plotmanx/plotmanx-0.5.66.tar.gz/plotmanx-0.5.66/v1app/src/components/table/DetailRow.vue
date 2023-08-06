<template>
  <div @click="onClick">
    <div class="inline field">
      <label>Address: </label>
      <span>{{ rowData.address }}</span>
    </div>
    <div class="inline field">
      <label>Amount: </label>
      <span>{{ rowData.amount }}</span>
    </div>
  </div>
</template>

<script>

export default {
  props: {
    rowData: {
      type: Object,
      required: true
    },
    rowIndex: {
      type: Number,
      default () {
        return 0
      }
    }
  },
  computed: {

  },
  methods: {
    onClick (event) {
      console.log("my-detail-row: on-click", event.target)
    }
  }
}
</script>
