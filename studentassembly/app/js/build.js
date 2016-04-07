import Vue from 'vue'
import VueResource from 'vue-resource'
import { sync } from 'vuex-router-sync'

import App from './app.vue'
import store from './vuex/store'
import router from './router'
import { initResource } from './resource'

Vue.config.debug = location.hostname === 'localhost'

console.log(Vue.config)

sync(store, router)

Vue.use(VueResource)
initResource(Vue)

router.start(App, '#app')
