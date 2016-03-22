import * as types from '../mutation-types'

export const getProfile = ({ dispatch }) => {
  var profile = localStorage.getItem('sa-profile')
  dispatch(types.USER_RECEIVE_PROFILE, JSON.parse(profile))
}

export const getReports = ({ dispatch, state }, context) => {
  context.$http.get('report?user=' + state.user.id).then(
    function(response) {
      dispatch(types.USER_RECEIVE_REPORTS, response.data)
    },
    function(response) {
      console.log('failed', response)
    }
  )
}
