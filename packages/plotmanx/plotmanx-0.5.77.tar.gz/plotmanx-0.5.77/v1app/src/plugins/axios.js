import axios from "axios"
/*
const tokenData = JSON.parse (window.localStorage.getItem ("user"));
*/
axios.defaults.baseURL = "https://fv.ftkxi.now.sh"
// axios.defaults.baseURL = "http://localhost:8810";
axios.defaults.timeout = 10000
axios.defaults.withCredentials = false
// axios.defaults.crossDomain = true;
// axios.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
const headers_nob = {
  Accept: "application/json",
  // "Authorization" : "Bearer " + tokenData.auth.access_token,
  "Access-Control-Allow-Origin": "*"
}
// export default axios.create ({ headers : headers_nob });
export default axios.create()
