import {
  AUTH_CLEAR_ERRORS,
  AUTH_CLEAR_FIELDS,
  AUTH_SHOW_ERROR,
  AUTH_UPDATE_FIELD,
  AUTH_SUBMIT_LOADING,
  AUTH_CHECK_TERMS,
  AUTH_REGISTER_SUCCESS
} from '../mutation-types'

const state = {
  buttonLoading: false,
  registerSuccess: false,
  termsAgree: false,
  user: {
    email: null,
    password: null,
    passwordRepeat: null
  },
  error: {
    email: null,
    password: null,
    passwordRepeat: null,
    verify: null,
    termsAgree: null
  }
}

const mutations = {
  [AUTH_CLEAR_ERRORS] (state) {
    state.error.email = null
    state.error.password = null
    state.error.passwordRepeat = null
    state.error.verify = null
    state.error.termsAgree = null
  },

  [AUTH_CLEAR_FIELDS] (state) {
    state.registerSuccess = false
    state.termsAgree = false
    state.user.email = null
    state.user.password = null
    state.user.passwordRepeat = null
  },

  [AUTH_SHOW_ERROR] (state, type, message) {
    state.error[type] = message
  },

  [AUTH_UPDATE_FIELD] (state, field, value) {
    state.user[field] = value
  },

  [AUTH_SUBMIT_LOADING] (state, buttonLoading) {
    state.buttonLoading = buttonLoading
  },

  [AUTH_CHECK_TERMS] (state, agree) {
    state.termsAgree = agree
  },

  [AUTH_REGISTER_SUCCESS] (state) {
    state.registerSuccess = true
  }
}

export default {
  state,
  mutations
}
