<template>
  <v-sheet
    :color="c6_primary"
    class="text-center"
    height="90vh">
    <v-btn class="mt-6" text color="error" @click="$emit('close')">{{ $t("p_close") }}</v-btn>
    <!--    <v-container
            style="align-items: flex-start !important;"
            fluid>-->
    <v-simple-table
      dense
      fixed-header
      height="500px">
      <template v-slot:default>
        <thead>
          <tr>
            <th class="text-left">
              T
            </th>
            <th class="text-left">
              Console Message
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(v, i) in items"
              :key="i">
            <td class="text-left"> {{ v.type }} <p>({{ v.message }})</p></td>
            <td class="text-left lvxwordwrap">{{ string_release(v.data) }}</td>
          </tr>
        </tbody>
      </template>

    </v-simple-table>
    <v-btn class="mt-6" text color="error" @click="clearcb">Clear</v-btn>
    <!--    </v-container>-->
  </v-sheet>
</template>

<script>

import string_tx from "@/api/mixins/string_tx"

export default {
  name: "Debug",
  mixins: [string_tx],
  computed: {
    items() {
      return this.$store.getters["wallet/list_events"]
    }
  },
  mounted() {
    this.$nextTick(() => {
      /*

       this.appendItem("error f1", "internal", "foisjdfjsoijfoiiiojsfio jsdifjsoiejfoijesi48273984728974982j2h4kj2h34h2j hjkhkj342h34k2h 23k h42k3 h4kj23jk4h2k3jh4323h 423482882829982 block.")
       this.appendItem("error f12", "internal", "foisjdifjsoijfoiisiojsfiojsdoifjsoiejfoijesiof482739847289749827934798274892739847 joisdj ifosdj f28734982734j2h4kj2h34h2jhjkh h2kj342h34k2h 23k h42k3 h4kj23jk4h2k3jh4323h423482882829982 block.")
       this.appendItem("error f223", "internal", "foisjdifjsoijfoiisiojsfiojs doifjsoiejfoijesiof4827398472897498279347 98274892739847 joisdj ifosdj f28734982734j2h4kj2h34h2jhjkh h2kj342h34k2h 23k h42k3 h4kj23jk4h2k3jh4323h423482882829982 block.")
       this.appendItem("error f8732", "internal", "foisjdifjsoijfoiisiojsfiojsdoifjsoiejfoijesiof482739847289749827934798274892739847 joisdj ifosdj f28734982734j2h4kj2h34h2jhjkh h2kj342h34k2h 23k h42k3 h4kj23jk4h2k3jh4323h423482882829982 block.")
       this.appendItem("error f7532", "internal", "foisjdifjso ijfoiisiojsfiojsdoifjsoiejfoijesiof48273984728974982793479827489273j f28734982734j2h4kj2h34h2jhj2h34k2h 23k h42k3 h4kj23jk4h2k3jh4323h423482882829982 block.")
       this.appendItem("error f32", "internal", "foisjdifjsoijfoiisio jsfiojsdoifjsoiejfoijesiof482739847289749 827934798274892739847734982734j2h4kj2h34h2jhjkhh2kj342h34k2h 23k h42k3 h4kj23jk4h2k3jh4323h423482882829982 block.")
       this.appendItem("error f31", "internal", "foisjdifjsoijfoiisiojsfiojsdo ifjsoiejfoijesiof48273984728974982793 4798274892739847oisd982734j2h4kj2h34h2jhjkhh2kj342h34k2h 23k h42k3 h4kj23jk4h2k3jh4323h423482882829982 block.")
       this.appendItem("error f463", "internal", "foisjdifjsoijfoiisiojsfiojsd oifjsoiejfoijesiof482739847289749827934798274892739847 joisdj ifosdj f28734982734j2h4kj2h34h2jhjkh h2kj342h34k2h 23k h42k3 h4kj23jk4h2k3jh4323h423482882829982 block.")
       this.appendItem("error f833", "internal", "foisjdifjsoijfoiisiojsfiojsdoifjsoiejfo ijesiof482739847289749827934798274892739847 joisdj ifosdj f28734982734j2h4kj2h34h2jhjkh h2kj342h34k2h 23k h42k3 h4kj23jk4h2k3jh4323h423482882829982 block.")
       this.appendItem("error f3661", "internal", "foisjdifjsoijfoiisiojsfioj sdoifjsoiejfoijesiof482739847289749827934798274892739847 joisdj ifosdj f28734982734j2h4kj2h34h2jhjkh h2kj342h34k2h 23k h42k3 h4kj23jk4h2k3jh4323h423482882829982 block.")

   */
    })
  },
  methods: {
    clearcb() {
      this.$store.dispatch("wallet/clearEvents")
    },
    string_release(dat) {
      if (typeof dat === "string" || typeof dat === "number") {
        return dat
      } else {
        return JSON.stringify(dat)
      }
    },
    appendItem(msg, whatsort, dat) {
      this.$store.dispatch("wallet/newEventTransaction", {
        msg,
        whatsort,
        dat
      })
    },
    onScroll() {
      this.scrollTop++
    }
  }
}
</script>

<style lang="scss">
.lvxwordwrap {
  overflow-wrap: anywhere;
  word-wrap: break-word;
  hyphens: auto;
}

.v-data-table > .v-data-table__wrapper > table {
  table-layout: fixed;
  word-wrap: break-word;
  tr > td:first-child,
  tr > th:first-child {
    width: 100px;
  }
}

/*
.v-data-table > .v-data-table__wrapper {
  color: var(--color-blue-light);
  background-color: var(--color-bg);
}*/

</style>
