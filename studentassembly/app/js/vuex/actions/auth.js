import * as types from '../mutation-types'

export const register = ({ dispatch, state }, context) => {
  dispatch(types.AUTH_CLEAR_ERRORS)
  dispatch(types.BUTTON_SUBMIT_LOADING, true)

  if (state.auth.user.agreeTerms) {
    context.$http.post('register', state.auth.user).then(
      (response) => {
        dispatch(types.BUTTON_SUBMIT_LOADING, false)
        state.route.path = '/login'
        dispatch(
          types.AUTH_SHOW_SUCCESS,
          'register',
          "We've sent a link to your email so you'll be verified before logging in."
        )
      },
      (response) => {
        for (let key in response.data) {
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
    dispatch(
      types.AUTH_SHOW_ERROR,
      'agreeTerms',
      "Sorry, you have to agree with our house rules to register."
    )
    dispatch(types.BUTTON_SUBMIT_LOADING, false)
  }
}

export const login = ({ dispatch, state }, context) => {
  dispatch(types.AUTH_CLEAR_ERRORS)
  dispatch(types.BUTTON_SUBMIT_LOADING, true)

  context.$http.post('token_auth', state.auth.user).then(
    (response) => {
      var user = JSON.parse(atob(response.data.token.split('.')[1]))
      dispatch(types.BUTTON_SUBMIT_LOADING, false)
      dispatch(types.AUTH_LOGIN_SUCCESS, user)
      state.route.path = '/profile'
    },
    (response) => {
      for (let key in response.data) {
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

export const refreshToken = ({ dispatch, state }, context, redir) => {
  const token = localStorage.getItem('sa-token')
  context.$http.post('token_refresh', { token: token }).then(
    (response) => {
      var user = JSON.parse(atob(response.data.token.split('.')[1]))
      dispatch(types.AUTH_LOGIN_SUCCESS, user)
      state.route.path = redir.to.path
    },
    (response) => {
      state.route.path = '/404'
    }
  )
}

export const verifyAccount = ({ dispatch, state }, context, token) => {
  context.$http.post('verify_account', { token: token }).then(
    (response) => {
      state.route.path = '/login'
      dispatch(
        types.AUTH_SHOW_SUCCESS,
        'verifyAccount',
        "Your account has been verified! Log in to start using Student Assembly."
      )
    },
    (response) => {
      state.route.path = '/login'
      for (let key in response.data) {
        if (key === 'error') {
          dispatch(types.AUTH_SHOW_ERROR, 'other', response.data[key])
        }
      }
    }
  )
}

export const resendVerification = ({ dispatch, state }, context) => {
  dispatch(types.AUTH_CLEAR_ERRORS)
  dispatch(types.BUTTON_SUBMIT_LOADING, true)

  context.$http.post('resend_verification', { email: state.auth.user.email }).then(
    (response) => {
      state.route.path = '/login'
      dispatch(
        types.AUTH_SHOW_SUCCESS,
        'resendVerification',
        "Your new verification link has been sent to your email!"
      )
      dispatch(types.BUTTON_SUBMIT_LOADING, false)
    },
    (response) => {
      for (let key in response.data) {
        if (key === 'error') {
          dispatch(types.AUTH_SHOW_ERROR, 'email', response.data[key])
        }
      }
      dispatch(types.BUTTON_SUBMIT_LOADING, false)
    }
  )
}

export const sendResetPasswordLink = ({ dispatch, state }, context) => {
  dispatch(types.AUTH_CLEAR_ERRORS)
  dispatch(types.BUTTON_SUBMIT_LOADING, true)

  context.$http.post('send_password_reset_link', { email: state.auth.user.email }).then(
    (response) => {
      dispatch(
        types.AUTH_SHOW_SUCCESS,
        'sendResetPasswordLink',
        "Your reset password link has been sent to your email."
      )
      dispatch(types.BUTTON_SUBMIT_LOADING, false)
    },
    (response) => {
      for (let key in response.data) {
        if (key === 'error') {
          dispatch(types.AUTH_SHOW_ERROR, 'email', response.data[key])
        }
      }
      dispatch(types.BUTTON_SUBMIT_LOADING, false)
    }
  )
}

export const resetPassword = ({ dispatch, state }, context) => {
  dispatch(types.AUTH_CLEAR_ERRORS)
  dispatch(types.BUTTON_SUBMIT_LOADING, true)

  const token = state.route.query.token.split('.')

  let data = {
    username: atob(token[0]),
    token: atob(token[1]),
    password: state.auth.user.password
  }

  context.$http.patch('reset_password', data).then(
    (response) => {
      dispatch(types.BUTTON_SUBMIT_LOADING, false)
      state.route.path = '/login'
      dispatch(
        types.AUTH_SHOW_SUCCESS,
        'resetPassword',
        "Your password has been reset! Log in with your new password to start using Student Assembly."
      )
    },
    (response) => {
      for (let key in response.data) {
        if (key === 'error') {
          dispatch(types.AUTH_SHOW_ERROR, 'other', response.data[key])
        }
      }
      dispatch(types.BUTTON_SUBMIT_LOADING, false)
    }
  )
}

export const logout = ({ dispatch, state }) => {
  localStorage.removeItem('sa-token')
  localStorage.removeItem('sa-profile')
  dispatch(types.AUTH_LOGOUT_SUCCESS)
  state.route.path = '/login'
}
