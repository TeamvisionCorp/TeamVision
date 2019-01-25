// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import router from './router'
import store from './store'
import 'jquery/dist/jquery'
import './assets/bootstrap/dist/css/bootstrap.min.css'
import './assets/bootstrap/dist/js/bootstrap'
import iView from 'iview'
import 'iview/dist/styles/iview.css'
import './assets/teamcat/global/less/global.less'
import '../src/assets/teamcat/global/less/MyIviewTheme.less'
import '@progress/kendo-ui'
import '@progress/kendo-theme-material/dist/all.css'
// import '@progress/kendo-theme-default/dist/all.css'
import '@progress/kendo-ui/js/messages/kendo.messages.zh-cn.js'
// import VueQuillEditor from 'vue-quill-editor'

require('font-awesome-webpack')
axios.defaults.withCredentials = true
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'

// axios.defaults.headers.sessionId='afdgmgwex411zlj8r8wwfidbl6171ki7'
// axios.defaults.headers.sessionId = 'genupzea4d5xvjwp087vwr0bdwo59drl'
Vue.prototype.$axios = axios
Vue.config.productionTip = false
Vue.use(iView)
// Vue.use(VueQuillEditor)

/* eslint-disable no-new */

const app = new Vue({
  router,
  store,
  axios,
  VueAxios,
  ...App
})
app.$mount('#teamvision')
