import * as types from '../mutation-types'

export const register = ({ dispatch, state }, context) => {
  dispatch(types.AUTH_CLEAR_ERRORS)
  dispatch(types.BUTTON_SUBMIT_LOADING, true)

  if (state.auth.user.password === state.auth.user.passwordRepeat) {
    if (state.auth.termsAgree) {
      context.$http.post('register', state.auth.user).then(
        function(response) {
          dispatch(types.BUTTON_SUBMIT_LOADING, false)
          dispatch(types.AUTH_REGISTER_SUCCESS)
        },
        function(response) {
          for (var key in response.data) {
            if (key === 'email') {
              dispatch(types.AUTH_SHOW_ERROR, 'email', response.data[key])
            }
            if (key === 'password') {
              dispatch(types.AUTH_SHOW_ERROR, 'password', response.data[key])
            }
          }
          dispatch(types.BUTTON_SUBMIT_LOADING, false)
        }
      )
    }
    else {
      dispatch(types.AUTH_SHOW_ERROR, 'termsAgree', "Sorry, you have to agree with our house rules to register.")
      dispatch(types.BUTTON_SUBMIT_LOADING, false)
    }
  }
  else {
    dispatch(types.AUTH_SHOW_ERROR, 'passwordRepeat', "Oops, the passwords did not match.")
    dispatch(types.BUTTON_SUBMIT_LOADING, false)
  }
}

export const login = ({ dispatch, state }, context) => {
  dispatch(types.AUTH_CLEAR_ERRORS)
  dispatch(types.BUTTON_SUBMIT_LOADING, true)

  context.$http.post('token_auth', state.auth.user).then(
    function(response) {
      var user = JSON.parse(atob(response.data.token.split('.')[1]))
      dispatch(types.BUTTON_SUBMIT_LOADING, false)
      dispatch(types.AUTH_LOGIN_SUCCESS, user)
      state.route.path = '/profile'
    },
    function(response) {
      for (var key in response.data) {
        if (key === 'non_field_errors') {
          dispatch(types.AUTH_SHOW_ERROR, 'email', response.data[key])
          dispatch(types.AUTH_SHOW_ERROR, 'password', response.data[key])
        }
        if (key === 'email') {
          dispatch(types.AUTH_SHOW_ERROR, 'email', response.data[key])
        }
        if (key === 'password') {
          dispatch(types.AUTH_SHOW_ERROR, 'password', response.data[key])
        }
        if (key === 'detail') {
          dispatch(types.AUTH_SHOW_ERROR, 'verify', response.data[key])
        }
      }
      dispatch(types.BUTTON_SUBMIT_LOADING, false)
    }
  )
}

export const logout = ({ dispatch }) => {
  localStorage.removeItem('sa-token')
  localStorage.removeItem('sa-profile')
  dispatch(types.AUTH_LOGOUT_SUCCESS)
}
