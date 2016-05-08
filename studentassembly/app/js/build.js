import Vue from 'vue'
import { sync } from 'vuex-router-sync'

import App from './app.vue'
import store from './vuex/store'
import router from './router'
import { initResource } from './resource'
import { registerFilters } from './filters'

Vue.config.debug = location.hostname === 'localhost'
sync(store, router)
initResource()
registerFilters()

router.start(App, '#app')
