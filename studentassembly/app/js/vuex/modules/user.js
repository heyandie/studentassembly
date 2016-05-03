import {
  AUTH_LOGIN_SUCCESS,
  AUTH_LOGOUT_SUCCESS,
  USER_RECEIVE_PROFILE,
  USER_RECEIVE_REPORTS
} from '../mutation-types'

function defaultUserState () {
  return {
    id: null,
    alias: null,
    reports: [],
    ratings: [],
    upvoted: [],
    following: []
  }
}

const state = defaultUserState()

const mutations = {
  [AUTH_LOGIN_SUCCESS] (state, user) {
    state.id = user.user_id
    state.alias = user.alias
  },

  [AUTH_LOGOUT_SUCCESS] (state) {
    let logoutState = defaultUserState()
    Object.keys(logoutState).forEach((key) => {
      state[key] = logoutState[key]
    })
  },

  [USER_RECEIVE_PROFILE] (state, profile) {
    state.id = profile.id
    state.alias = profile.alias
  },

  [USER_RECEIVE_REPORTS] (state, data) {
    state.reports = data.reports
    state.upvoted = data.upvoted
    state.following = data.following
  }
}

export default {
  state,
  mutations
}
