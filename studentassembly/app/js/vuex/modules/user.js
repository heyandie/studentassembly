import {
  AUTH_LOGIN_SUCCESS,
  AUTH_LOGOUT_SUCCESS,
  USER_RECEIVE_REPORTS
} from '../mutation-types'

const state = {
  id: null,
  username: null,
  email: null,
  contact: {
    name: null,
    mobile: null
  },
  reports: []
}

const mutations = {
  [AUTH_LOGIN_SUCCESS] (state, user) {
    state.id = user.user_id
    state.username = user.username
    state.email = user.email
  },

  [AUTH_LOGOUT_SUCCESS] (state) {
    state.id = null
    state.username = null
    state.email = null
  },

  [USER_RECEIVE_REPORTS] (state, reports) {
    state.reports = reports
  }
}

export default {
  state,
  mutations
}
