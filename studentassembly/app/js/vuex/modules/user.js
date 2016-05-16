import {
  AUTH_LOGIN_SUCCESS,
  AUTH_LOGOUT_SUCCESS,
  USER_RECEIVE_PROFILE,
  USER_RECEIVE_REPORTS,
  USER_RECEIVE_RATINGS,
  USER_UPDATE_REPORTS,
  USER_UPDATE_RATINGS,
  USER_UPDATE_UPVOTED,
  USER_UPDATE_FOLLOWING
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

// Consult API for keys
const basicReportKeys = [
  'id', 'category', 'text', 'created_at', 'updated_at',
  'deleted_at', 'allow_publish', 'is_approved', 'school',
  'status', 'school_id', 'alias'
]

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
  },

  [USER_RECEIVE_RATINGS] (state, data) {
    state.ratings = data
  },

  [USER_UPDATE_REPORTS] (state, data) {
    console.log(data)
    let report = {}
    basicReportKeys.forEach((key) => {
      report[key] = data[key]
    })
    state.reports.unshift(report)
  },

  [USER_UPDATE_RATINGS] (state, data) {
    state.ratings = data
  },

  [USER_UPDATE_UPVOTED] (state, method, data) {
    let upvoted = {
      id: data.id
    }

    if (method === 'upvote') {
      basicReportKeys.forEach((key) => {
        upvoted[key] = data[key]
      })
      state.upvoted.unshift(upvoted)
    }
    else {
      let index = state.upvoted.findIndex((element, index, array) => {
        return element.id === upvoted.id
      })
      state.upvoted.splice(index, 1)
    }
  },

  [USER_UPDATE_FOLLOWING] (state, method, data) {
    let following = {
      id: data.id
    }

    if (method === 'follow') {
      basicReportKeys.forEach((key) => {
        following[key] = data[key]
      })
      state.following.unshift(following)
    }
    else {
      let index = state.following.findIndex((element, index, array) => {
        return element.id === following.id
      })
      state.following.splice(index, 1)
    }
  }
}

export default {
  state,
  mutations
}
