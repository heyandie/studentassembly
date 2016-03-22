import Vue from 'vue'
import Vuex from 'vuex'

import * as types from './mutation-types'

import auth from './modules/auth'
import user from './modules/user'
import report from './modules/report'

Vue.use(Vuex)

const persistUserState = {
  onMutation ({ type, payload }, state) {
    if (type === types.AUTH_LOGIN_SUCCESS ||
        type === types.USER_RECEIVE_REPORTS) {
      localStorage.setItem('sa-profile', JSON.stringify(state.user))
    }
  }
}

export default new Vuex.Store({
  modules: {
    auth,
    user,
    report
  },
  middlewares: [persistUserState]
})
