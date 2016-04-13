import * as types from '../mutation-types'

export const getSchools = ({ dispatch }, context) => {
  context.$http.get('schools').then(
    function(response) {
      dispatch(types.REPORT_RECEIVE_SCHOOLS, response.data)
    },
    function(response) {
      console.log('Retrieving list of schools failed.')
    }
  )
}

export const getCategories = ({ dispatch }, context) => {
  context.$http.get('categories').then(
    function(response) {
      dispatch(types.REPORT_RECEIVE_CATEGORIES, response.data)
    },
    function(response) {
      console.log('Retrieving list of categories failed.')
    }
  )
}

export const getReport = ({ dispatch, state }, context) => {
  dispatch(types.BUTTON_SUBMIT_LOADING, true)

  context.$http.get('report/' + state.report.view.id).then(
    function(response) {
      dispatch(types.REPORT_RECEIVE_REPORT, response.data)
      dispatch(types.BUTTON_SUBMIT_LOADING, false)
    },
    function(response) {
      console.log('Failed to retrieve report.')
      state.route.path = '/index'
    }
  )
}

export const submitReport = ({ dispatch, state }, context) => {
  dispatch(types.BUTTON_SUBMIT_LOADING, true)

  context.$http.post('report/', state.report.request).then(
    function (response) {
      dispatch(types.BUTTON_SUBMIT_LOADING, false)
      state.route.path = '/profile'
    },
    function (response) {
      for (var key in response.data) {
        if (key === 'school') {
          dispatch(types.REPORT_SHOW_ERROR, 'school', response.data[key])
        }
        if (key === 'category') {
          dispatch(types.REPORT_SHOW_ERROR, 'category', response.data[key])
        }
        if (key === 'text') {
          dispatch(types.REPORT_SHOW_ERROR, 'text', response.data[key])
        }
      }
      dispatch(types.BUTTON_SUBMIT_LOADING, false)
    }
  )
}
