import Vue from 'vue'
import VueResource from 'vue-resource'
import { sync } from 'vuex-router-sync'

import App from './app.vue'
import store from './vuex/store'
import router from './router'
import { initResource } from './resource'

Vue.config.debug = process.env.NODE_ENV !== 'production'
Vue.config.devtools = process.env.NODE_ENV !== 'production'

console.log(Vue.config.debug)

sync(store, router)

Vue.use(VueResource)
initResource(Vue)

router.start(App, '#app')
