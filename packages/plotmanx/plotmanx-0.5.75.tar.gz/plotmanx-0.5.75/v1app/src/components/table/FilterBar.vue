<template>
  <div class="filter-bar ui basic segment grid row">
    <div class="ui form">
      <div class="inline field">
        <label>Search for:</label>
        <input v-model="filterText"
               placeholder="name, nickname, or email"
               class="three wide column"
               type="text"
               @keyup.enter="doFilter"/>
        <button class="ui primary button" @click="doFilter">Go</button>
        <button class="ui button" @click="resetFilter">Reset</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      filterText: ""
    }
  },
  methods: {
    doFilter () {
      this.$emit("filter-set", this.filterText)
    },
    resetFilter () {
      this.filterText = ""
      this.$emit("filter-reset")
    }
  }
}
</script>
