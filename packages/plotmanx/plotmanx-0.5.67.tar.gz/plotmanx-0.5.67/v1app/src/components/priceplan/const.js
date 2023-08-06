const BASE_REF_NAME = "planx"

export const TYPESC = Object.freeze({
  BASE_REF_NAME
})

export const TYPESCMIX = {
  created() {
    this.TYPESC = TYPESC
  }
}
