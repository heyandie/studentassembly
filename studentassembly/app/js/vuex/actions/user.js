import * as types from '../mutation-types'

export const getProfile = ({ dispatch }) => {
  let profile = localStorage.getItem('sa-profile')
  if (profile)
    dispatch(types.USER_RECEIVE_PROFILE, JSON.parse(profile))
}

export const getReports = ({ dispatch, state }, context) => {
  if (!state.user.reports.length) {
    dispatch(types.BUTTON_SUBMIT_LOADING, true)
    context.$http.get('report?user=' + state.user.id + '&upvoted=True&following=True').then(
      (response) => {
        dispatch(types.USER_RECEIVE_REPORTS, response.data)
        dispatch(types.BUTTON_SUBMIT_LOADING, false)
      },
      (response) => {
        console.log('Failed to retrieve user reports.')
      }
    )
  }
}

export const getRatings = ({ dispatch, state }, context) => {
  if (!state.user.ratings.length) {
    dispatch(types.BUTTON_SUBMIT_LOADING, true)
    context.$http.get('rating?user=' + state.user.id).then(
      (response) => {
        dispatch(types.USER_RECEIVE_RATINGS, response.data)
        dispatch(types.BUTTON_SUBMIT_LOADING, false)
      },
      (response) => {
        console.log('Failed to retrieve user ratings.')
      }
    )
  }
}
