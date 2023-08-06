// plugins/svg-sprite-loader.js
// import only in browser
if (process.BROWSER_BUILD) {
  // import all svgs
  const files = require.context("~assets/svg", false, /\.svg$/)
  files.keys().forEach(files)
}
