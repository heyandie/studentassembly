import {
  BUTTON_SUBMIT_LOADING,
  AUTH_CLEAR_ERRORS,
  AUTH_CLEAR_FIELDS,
  AUTH_SHOW_ERROR,
  AUTH_UPDATE_FIELD,
  AUTH_CHECK_TERMS,
  AUTH_REGISTER_SUCCESS
} from '../mutation-types'

function defaultAuthErrors () {
  return {
    email: null,
    password: null,
    passwordRepeat: null,
    verify: null,
    termsAgree: null
  }
}

function defaultUserRequest () {
  return {
    email: null,
    password: null,
    passwordRepeat: null
  }
}

const state = {
  buttonLoading: false,
  registerSuccess: false,
  termsAgree: false,
  user: defaultUserRequest(),
  error: defaultAuthErrors()
}

const mutations = {
  [AUTH_CLEAR_ERRORS] (state) {
    state.error = defaultAuthErrors()
  },

  [AUTH_CLEAR_FIELDS] (state) {
    state.buttonLoading = false
    state.registerSuccess = false
    state.termsAgree = false
    state.user = defaultUserRequest()
  },

  [AUTH_SHOW_ERROR] (state, type, message) {
    state.error[type] = message
  },

  [AUTH_UPDATE_FIELD] (state, field, value) {
    state.user[field] = value
  },

  [BUTTON_SUBMIT_LOADING] (state, buttonLoading) {
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
