import * as types from '../mutation-types'

export const getReports = ({ dispatch, state }, context) => {
  context.$http.get('report/' + state.user.id).then(
    function(response) {
      dispatch(types.USER_RECEIVE_REPORTS, response.data)
    },
    function(response) {
      console.log('failed', response)
    }
  )
}
