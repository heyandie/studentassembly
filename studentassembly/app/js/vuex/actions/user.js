import * as types from '../mutation-types'

export const getProfile = ({ dispatch }) => {
  let profile = localStorage.getItem('sa-profile')
  if (profile)
    dispatch(types.USER_RECEIVE_PROFILE, JSON.parse(profile))
}

export const getReports = ({ dispatch, state }, context) => {
  dispatch(types.BUTTON_SUBMIT_LOADING, true)
  context.$http.get('report?&user=' + state.user.id).then(
    (response) => {
      dispatch(types.USER_RECEIVE_REPORTS, response.data)
      dispatch(types.BUTTON_SUBMIT_LOADING, false)
    },
    (response) => {
      console.log('Retrieving user reports failed.')
    }
  )
}
