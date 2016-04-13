import {
  AUTH_LOGIN_SUCCESS,
  AUTH_LOGOUT_SUCCESS,
  USER_RECEIVE_PROFILE,
  USER_RECEIVE_REPORTS
} from '../mutation-types'

const state = {
  id: null,
  alias: null,
  report_count: 0,
  reports: []
}

const mutations = {
  [AUTH_LOGIN_SUCCESS] (state, user) {
    state.id = user.user_id
    state.alias = user.alias
    state.report_count = user.report_count
  },

  [AUTH_LOGOUT_SUCCESS] (state) {
    state.id = null
    state.alias = null
    state.report_count = 0
    state.reports = []
  },

  [USER_RECEIVE_PROFILE] (state, profile) {
    state.id = profile.id
    state.alias = profile.alias
    state.reports = profile.reports
    state.report_count = profile.report_count
  },

  [USER_RECEIVE_REPORTS] (state, reports) {
    state.reports = reports
    state.report_count = reports.length
  }
}

export default {
  state,
  mutations
}
