<template>
  <section id="indexbox" class="indexcolor">
    <div class="backee home">
      <!--<bg-jpflowani
        title="FORSAGE SAKURA"
        overlayer="n1"
      />-->
    </div>
    <div class="box-wrap center">
      <v-main>
        <v-layout align-center class="flex-column">
          <v-card
            v-if="ready_to_share"
            class="qrcard mr-4 ml-4 mb-6 mt-16 mt-lg-16"
            elevation="11">
            <v-card-title>
              <img
                style="margin-right: 10px"
                src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAMJlWElmTU0AKgAAAAgABwESAAMAAAABAAEAAAEaAAUAAAABAAAAYgEbAAUAAAABAAAAagEoAAMAAAABAAIAAAExAAIAAAARAAAAcgEyAAIAAAAUAAAAhIdpAAQAAAABAAAAmAAAAAAAAABIAAAAAQAAAEgAAAABUGl4ZWxtYXRvciAzLjcuNAAAMjAyMDoxMDoxNyAxODoxMDo2MgAAA6ABAAMAAAABAAEAAKACAAQAAAABAAAAEKADAAQAAAABAAAAEAAAAAA4wwn8AAAACXBIWXMAAAsTAAALEwEAmpwYAAAEJGlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNi4wLjAiPgogICA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgICAgICAgICB4bWxuczpleGlmPSJodHRwOi8vbnMuYWRvYmUuY29tL2V4aWYvMS4wLyIKICAgICAgICAgICAgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIgogICAgICAgICAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyIKICAgICAgICAgICAgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIj4KICAgICAgICAgPGV4aWY6Q29sb3JTcGFjZT4xPC9leGlmOkNvbG9yU3BhY2U+CiAgICAgICAgIDxleGlmOlBpeGVsWERpbWVuc2lvbj4xNjwvZXhpZjpQaXhlbFhEaW1lbnNpb24+CiAgICAgICAgIDxleGlmOlBpeGVsWURpbWVuc2lvbj4xNjwvZXhpZjpQaXhlbFlEaW1lbnNpb24+CiAgICAgICAgIDx4bXA6Q3JlYXRvclRvb2w+UGl4ZWxtYXRvciAzLjcuNDwveG1wOkNyZWF0b3JUb29sPgogICAgICAgICA8eG1wOk1vZGlmeURhdGU+MjAyMC0xMC0xN1QxODoxMDo2MjwveG1wOk1vZGlmeURhdGU+CiAgICAgICAgIDx0aWZmOlJlc29sdXRpb25Vbml0PjI8L3RpZmY6UmVzb2x1dGlvblVuaXQ+CiAgICAgICAgIDx0aWZmOkNvbXByZXNzaW9uPjA8L3RpZmY6Q29tcHJlc3Npb24+CiAgICAgICAgIDx0aWZmOk9yaWVudGF0aW9uPjE8L3RpZmY6T3JpZW50YXRpb24+CiAgICAgICAgIDx0aWZmOlhSZXNvbHV0aW9uPjcyPC90aWZmOlhSZXNvbHV0aW9uPgogICAgICAgICA8dGlmZjpZUmVzb2x1dGlvbj43MjwvdGlmZjpZUmVzb2x1dGlvbj4KICAgICAgICAgPGRjOnN1YmplY3Q+CiAgICAgICAgICAgIDxyZGY6QmFnLz4KICAgICAgICAgPC9kYzpzdWJqZWN0PgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KMmAN6AAAAhBJREFUOBF1U01rE1EUPZP5yswkwbah0wY7LQrSRSotWFAEFRduXYq4EFxUUQRB6MJFUbpQXIkbxR9QxI3QTStFsvJjYVGKIlqagrWobWIakjpJOjPX+0Yisc5cuLz37jvn3Hvfh4QIo8frt9CfnEIt2EYQALJkoe5NS2dyU7vhyu5AuPaCHjhJoN+wsMMCK3XgfbM7EhsXpNl1orpPVA2IZr9RHC66AoEOmNN234/jIxG743ssIAEid4vnMRYvUGsBErOJfZvnMRbZQuFmQUGPCjSZJao35Rg6olvIy9Z9HHOACmd2d4ATDujBh3uxKp0bLy7MHaGPFY/KRLT864/zQC9L9O7SwlgnVsz/a2F0tPc5Vhvy2twnGJoogDDgGNyGhqqhPWLOeKfIP4f4amL+hnnANhbflvGl6qL4s4m1rRaWlmsAa3TbXYdeT8xfiRU4fHTvRdrwwMeHXEZH1lRhp3nlcx4lgfxwFm4mc6dwdibbFgkrIJC0eP3ZAgayzmrJRW9ag6EqXLUCS7jOsO8NYFDHyL6+lGuk77YFwvsZP5e/fPz0wauoSNB8wp6kIMtMlpFi1zm7pjJ0KMk3qkD1tLFTfSd/zCw9eRMeopTWr2FkEPi8BStntsX/jin+T+BHiQR/sP0mhuwubJRLtznyMBSwJWkShZWnHHD59fkgwYiwolCBXPy6icZm9bxY/Abj07URyaImHQAAAABJRU5ErkJggg=="/>
              {{ $t("msg_invcard") }}
            </v-card-title>
            <qrcode :value="url_final" :options="{ width: 200, height:200 }"/>
            <v-card-title class="code_share">{{ my_invitation_code }}</v-card-title>
            <v-card-subtitle class="text-left brandname">Sakura</v-card-subtitle>
            <v-divider></v-divider>
            <v-card-text class="text-left">
              Share this code to earn your rewards now! or share with the full URL: {{ url_final }}
            </v-card-text>
            <v-card-actions>
              <v-btn v-if="!userRegistered" class="mt-6" text color="error" @click="open_sheet_referralcode">
                {{ $t("bnt_invcode") }}
              </v-btn>
              <v-btn class="mt-6" text color="error" @click="copy_code">{{ $t("bnt_share") }}</v-btn>
            </v-card-actions>
          </v-card>
          <v-card v-else class="qrcard mr-4 ml-4 mb-6 mt-16 mt-lg-16" elevation="11">
            <v-card-title>Not Ready</v-card-title>
            <v-card-text class="text-left">You are not ready to share code. Please get your referral code now.
            </v-card-text>
            <v-card-actions>
              <v-btn class="mt-6" text color="error" @click="open_sheet_referralcode">{{ $t("bnt_invcode") }}</v-btn>
            </v-card-actions>
          </v-card>
        </v-layout>
      </v-main>
    </div>
  </section>
</template>
<script>

import { EventBus } from "vue-backgrounds"
import nav from "@/api/mixins/tron/nav"
import mainForsafe from "@/api/mixins/tron/main975"

export default {
  layout: "bottom",
  mixins: [nav, mainForsafe],
  data() {
    return {
      ready_to_share: false,
      url_final: "------",
      my_invitation_code: "",
      genSecond: false
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.LanguageStart()
      const domain = process.env.domain
      const enter_code = "share?code="
      const in_code = this.$store.getters["forsage/show_invitation_code"]
      this.url_final = `${domain}/${enter_code}${in_code}`
      // console.log("share url: ", this.url_final, in_code)
      if (in_code.length > 0) {
        this.ready_to_share = true
      }
      this.$nextTick(() => {
        this.my_invitation_code = in_code
      })
      if (!this.ready_to_share && !this.genSecond) {
        this.genSecond = setInterval(() => {
          this.my_invitation_code = this.genSampleCode()
        }, 1000)
      }
    })
  },
  methods: {
    genSampleCode() {
      const chars = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
      const serialLength = 5
      let randomSerial = ""
      let i
      let randomNumber
      for (i = 0; i < serialLength; i = i + 1) {
        randomNumber = Math.floor(Math.random() * chars.length)
        randomSerial += chars.substring(randomNumber, randomNumber + 1)
      }
      return randomSerial
    },
    copy_code(e) {
      e.preventDefault()
      const that = this
      this.$copyText(this.url_final).then(function (e) {
        // alert ('Copied')
        // console.log (e)
        that.notificationSuccess(that.$t("n_copy"))
      }, function (e) {
        that.notificationError(e)
        // alert ('Can not copy')
        // console.log (e)
      })
    },
    open_sheet_referralcode(e) {
      e.preventDefault()
      EventBus.$emit("bottom_sheet_manual_enter")
    }
  }
}
</script>

<style scoped>
.backee {
  z-index: 0;
}

.qrcard {
  max-width: 500px;
}

@media screen and (max-width: 410px) {
  .qrcard {
    max-width: 360px;
  }
}
</style>
