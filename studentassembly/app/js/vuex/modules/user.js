import {
  AUTH_LOGIN_SUCCESS,
  AUTH_LOGOUT_SUCCESS,
  USER_RECEIVE_PROFILE,
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
  report_count: 0,
  reports: []
}

const mutations = {
  [AUTH_LOGIN_SUCCESS] (state, user) {
    state.id = user.user_id
    state.username = user.alias
    state.email = user.email
    state.report_count = user.report_count
  },

  [AUTH_LOGOUT_SUCCESS] (state) {
    state.id = null
    state.username = null
    state.email = null
    state.contact.name = null
    state.contact.mobile = null
    state.reports = []
  },

  [USER_RECEIVE_PROFILE] (state, profile) {
    state.id = profile.id
    state.username = profile.username
    state.email = profile.email
    state.contact = profile.contact
    state.reports = profile.reports
    state.report_count = profile.report_count
  },

  [USER_RECEIVE_REPORTS] (state, reports) {
    state.reports = reports
  }
}

export default {
  state,
  mutations
}
