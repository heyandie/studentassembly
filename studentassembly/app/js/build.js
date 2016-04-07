import Vue from 'vue'
import VueResource from 'vue-resource'
import { sync } from 'vuex-router-sync'

import App from './app.vue'
import store from './vuex/store'
import router from './router'
import { initResource } from './resource'

let env = process.env.NODE_ENV
Vue.config.debug = env !== 'undefined' && env !== 'production'
Vue.config.devtools = env !== 'undefined' && env !== 'production'

console.log(Vue.config.debug)

sync(store, router)

Vue.use(VueResource)
initResource(Vue)

router.start(App, '#app')
