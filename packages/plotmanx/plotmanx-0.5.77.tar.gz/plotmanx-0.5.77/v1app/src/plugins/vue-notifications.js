// This code will be injected before initializing the root App
import Vue from "vue"
import Noty from "noty"
// all themes
// mint, sunset, relax, nest, metroui, semanticui, light, bootstrap-v3, bootstrap-v4
// the only available themes
// mint, relax, metroui,
const options = {
  layout: "topCenter",
  theme: "relax",
  timeout: 3000
}

const module = {
  install: (Vue, opts) => {
    Vue.prototype.$notice = function (data) {
      return new Noty(Object.assign(options, opts, data)).show()
    }
  }
}

Vue.use(module)
