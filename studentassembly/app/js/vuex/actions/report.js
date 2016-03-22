import * as types from '../mutation-types'

export const getSchools = ({ dispatch }, context) => {
  context.$http.get('schools').then(
    function(response) {
      dispatch(types.REPORT_RECEIVE_SCHOOLS, response.data)
    },
    function(response) {
      console.log('failed', response)
    }
  )
}

export const getCategories = ({ dispatch }, context) => {
  context.$http.get('categories').then(
    function(response) {
      dispatch(types.REPORT_RECEIVE_CATEGORIES, response.data)
    },
    function(response) {
      console.log('failed', response)
    }
  )
}
