import Vue from 'vue'
import Vuex from 'vuex'
import Store from '../vendor/vuex-persist'

import auth from './modules/auth'
import user from './modules/user'

Vue.use(Vuex)

export default new Store({
  modules: {
    auth,
    user
  }
})
