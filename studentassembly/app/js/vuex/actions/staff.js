import * as types from '../mutation-types'

export const getStaff = ({ dispatch, state }, context) => {
  context.$http.get('staff').then(
    (response) => {
      dispatch(types.STAFF_RECEIVE_ALL, response.data)
    },
    (response) => {
      console.log('Failed to retrieve staff.')
    }
  )
}
