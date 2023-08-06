<template>
  <section id="indexbox" class="indexcolor">
    <div class="backee home">
      <!--  <bg-jpflowani
        :title="fulltitle"
        :topsubtitle="subtitle"
        overlayer="n921"
      />-->
    </div>
    <v-app class="box-wrap vapp center">
      <section class="section_tron_enter">
        <v-btn :color="status_button_co" class="line_btn" dark @click.native="goto_main">CONNECT</v-btn>

        <v-btn ref="aboutstory"
               class="line_btn"
               depressed
               color="transparent"
               to="#instruction"
               nuxt
               @click.stop="open_aboutstory">
          About
        </v-btn>

        <v-btn ref="langSelect" class="line_btn" depressed color="transparent" @click.stop="open_lang_selection">
          Languages
        </v-btn>

        <v-menu
            v-if="menuLang"
            ref="langmenu"
            :activator="$refs.langSelect.$el"
            :value="true"
            transition="slide-y-transition"
            tile
            offset-y>

          <v-list elevation="10">
            <v-list-item v-for="(val, k) in languages" :key="k" @click="onItemClicked(val)">
              <v-list-item-title align="left">{{ val.label }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </section>
      <v-bottom-sheet ref="aboutsheet" v-model="sheet" :value="aboutsheetshow" :retain-focus="false" inset
                      persistent>
        <v-sheet class="text-center" height="90vh">
          <v-btn class="mt-6" text color="error" @click="sheet = !sheet">{{ $t("p_close") }}</v-btn>
          <terms/>
        </v-sheet>
      </v-bottom-sheet>
    </v-app>
  </section>
</template>
<script>
import { TronLinkComponent, ImTokenComponent } from "vue-tronlink"
import nav from "@/api/mixins/tron/nav"
import string_tx from "@/api/mixins/string_tx"
import terms from "@/components/sheet/terms"

export default {
  layout: "cover",
  name: "Sakura",
  components: { terms },
  mixins: [TronLinkComponent, ImTokenComponent, nav, string_tx],
  data() {
    return {
      menuLang: false,
      sheet: false,
      aboutsheetshow: false,
      tronlinkinstalled: false,
      fulltitle: process.env.title,
      subtitle: process.env.subtitle
    }
  },
  computed: {
    status_button_co() {
      if (this.tronlinkinstalled) {
        return this.c3_primary
      } else {
        return this.c5_primary
      }
    }
  },
  watch: {
    aboutsheetshow() {
      this.$nextTick(() => {
        this.$refs.aboutsheet.showScroll()
        // either set :retain-focus="false" above or do this:
        // this.$nextTick(() => this.$refs.sheet.unbind());
      })
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.$on("notify_tron_not_install", () => {
        this.tronlinkinstalled = false
        console.log("detect done nil")
      })
      this.$on("notify_tron_installed", () => {
        this.tronlinkinstalled = true
        console.log("detect done ok")
      })
      this.$on("imtoken_on_detect", this.imtokenStyling)
      this.LanguageStart()
    })
  },
  methods: {
    imtokenStyling() {
      this.$emit("set_imtoken_style", {
        navigatorColor: this.c2_primary,
        navigationStyle: "default"
      })
    },
    goto_main() {
      if (this.tronlinkinstalled) {
        if (this.confirmDappChainID(process.env.network)) {
          this.straightInto("main")
          /*  if (this.on_imtoken) {
           this.imtokenSwitchAccount("TRON", (err) => {
           }, (address) => {
             this.straightInto("main")
           })
         } else {
           this.straightInto("main")
         } */
        } else {
          this.notificationError("This contract requires Nile network")
        }
      } else {
        this.notificationError(this.$t("msg_install"))
      }
    },
    open_aboutstory() {
      this.sheet = true
      // this.$nextTick(() => this.$refs.aboutstory.activate())
    },
    open_lang_selection() {
      if (this.menuLang && !this.$refs.langmenu.isContentActive) {
        // this.$refs.langmenu.isActive = true
        return
      }
      if (!this.menuLang) {
        this.menuLang = !this.menuLang
        if (this.menuLang) {
          this.$nextTick(() => this.$refs.langmenu.activate())
        }
      }
    },
    onItemClicked(evt) {
      this.menuLang = false
      if (!this.menuLang) {
        // this.$nextTick(() => this.$refs.langmenu.deactivate())
        this.ChangeLanguage(evt.key)
      }
    }
  }
}
</script>
<style scoped lang="scss">

.yd-rollnotice {
  background-color: transparent !important;
  //background: linear-gradient(to bottom, #56396d 1 %, rgba(76, 51, 93, 0.88) 4 %, rgba(54, 32, 65, 0.78) 98 %, #000 100 %);

  .yd-rollnotice-item {
    font-weight: lighter;
    font-size: 0.4em;
    color: white;

    span {
      color: red;
      font-weight: bold;
    }
  }
}
</style>
