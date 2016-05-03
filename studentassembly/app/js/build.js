import Vue from 'vue'
import { sync } from 'vuex-router-sync'

import App from './app.vue'
import store from './vuex/store'
import router from './router'
import { initResource } from './resource'

Vue.config.debug = location.hostname === 'localhost'
sync(store, router)
initResource()

// Vue.filter('wrap', function (value, begin, end) {
//   return begin + value + end
// })
// Vue.filter('currencyDisplay', {
//   // model -> view
//   // formats the value when updating the input element.
//   read: function(val) {
//     return '$'+val.toFixed(2)
//   },
//   // view -> model
//   // formats the value when writing to the data.
//   write: function(val, oldVal) {
//     var number = +val.replace(/[^\d.]/g, '')
//     return isNaN(number) ? 0 : parseFloat(number.toFixed(2))
//   }
// })

router.start(App, '#app')
