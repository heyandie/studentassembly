import {
  BUTTON_SUBMIT_LOADING,
  AUTH_CLEAR_ERRORS,
  AUTH_CLEAR_FIELDS,
  AUTH_SHOW_ERROR,
  AUTH_SHOW_SUCCESS,
  AUTH_UPDATE_FIELD,
  AUTH_TOGGLE_PASSWORD
} from '../mutation-types'

function defaultAuthErrors () {
  return {
    email: null,
    password: null,
    verify: null,
    agreeTerms: null,
    other: null
  }
}

function defaultAuthSuccess () {
  return {
    register: null,
    sendResetPasswordLink: null,
    resendVerification: null,
    verifyAccount: null,
    resetPassword: null
  }
}

function defaultUserRequest () {
  return {
    email: null,
    password: null,
    agreeTerms: false
  }
}

const state = {
  buttonLoading: false,
  passwordVisible: false,
  termsAgree: false,
  user: defaultUserRequest(),
  error: defaultAuthErrors(),
  success: defaultAuthSuccess()
}

const mutations = {
  [AUTH_CLEAR_ERRORS] (state) {
    state.error = defaultAuthErrors()
    state.success = defaultAuthSuccess()
  },

  [AUTH_CLEAR_FIELDS] (state) {
    state.user = defaultUserRequest()
    state.success = defaultAuthSuccess()

    state.buttonLoading = false
    state.passwordVisible = false
  },

  [AUTH_SHOW_SUCCESS] (state, type, message) {
    state.success[type] = message
  },

  [AUTH_SHOW_ERROR] (state, type, message) {
    state.error[type] = message
  },

  [AUTH_UPDATE_FIELD] (state, field, value) {
    state.user[field] = value
  },

  [AUTH_TOGGLE_PASSWORD] (state) {
    state.passwordVisible = !state.passwordVisible
  },

  [BUTTON_SUBMIT_LOADING] (state, buttonLoading) {
    state.buttonLoading = buttonLoading
  }
}

export default {
  state,
  mutations
}
