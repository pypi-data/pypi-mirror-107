<template>
  <section>
    <table class="table_proend tron">
      <tr class="headline">
        <th>Player</th>
        <th>Time</th>
        <th>Profit</th>
        <th>Visual</th>
      </tr>

      <tr v-for="(thd, n) in array_ex.slice(0, 10)" :key="n">
        <td>{{ thd.pid }}</td>
        <td> ---</td>
        <td class="profit">{{ thd.profit | changeprofit }}</td>
        <td>
          <div class="fuxContainer">
            <div v-for="(k,index) in thd.explain" :key="index" :class="classBoxCtl(index, thd.explain, thd.c)"
                 class="box">
            </div>
          </div>
        </td>
      </tr>
    </table>
  </section>
</template>

<script>

function classBoxCtl (index, arr, pick) {
  let bomb = false; let activeflag = false; let rewardflag = false
  if (_.indexOf(arr, index) > -1) {
    bomb = true
    if (pick === index) {
      activeflag = true
    }
  } else if (pick === index) {
    rewardflag = true
  }

  return {
    bomb,
    active: activeflag,
    reward: rewardflag
  }
}

export default {
  name: "FuseRFBox",
  props: ["gameId"],
  data () {
    return {}
  },
  computed: {
    array_ex: {
      get () {
        return this.$store.state._mines.block_history
      },
      set (newValue) {
      }
    }
  },
  methods: {
    ecp (str, maxLength, { side = "end", ellipsis = "..." } = {}) {
      if (str.length > maxLength) {
        switch (side) {
          case "start":
            return ellipsis + str.slice(-(maxLength - ellipsis.length))
          case "end":
          default:
            return str.slice(0, maxLength - ellipsis.length) + ellipsis
        }
      }
      return str
    }

  }
}
</script>

<style scoped>

</style>
