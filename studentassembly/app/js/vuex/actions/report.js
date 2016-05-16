import * as types from '../mutation-types'

export const getSchools = ({ dispatch }, context) => {
  context.$http.get('schools').then(
    (response) => {
      dispatch(types.REPORT_RECEIVE_SCHOOLS, response.data)
    },
    (response) => {
      console.log('Retrieving list of schools failed.')
    }
  )
}

export const getCategories = ({ dispatch }, context) => {
  context.$http.get('categories').then(
    (response) => {
      dispatch(types.REPORT_RECEIVE_CATEGORIES, response.data)
    },
    (response) => {
      console.log('Retrieving list of categories failed.')
    }
  )
}

export const getReport = ({ dispatch, state }, context) => {
  return context.$http.get('report/' + state.route.params.id).then(
    (response) => {
      dispatch(types.REPORT_RECEIVE_REPORT, response.data)
    },
    (response) => {
      console.log('Failed to retrieve report.')
      state.route.path = "/404"
    }
  )
}

export const getRelatedReports = ({ dispatch, state }, context) => {
  context.$http.get(
    'report?school=' + state.report.view.school_id +
    '&exclude=' + state.report.view.id +
    '&limit=3'
  ).then(
    (response) => {
      dispatch(types.REPORT_RECEIVE_RELATED, response.data.reports)
    },
    (response) => {
      console.log('Failed to retrieve related reports.')
    }
  )
}

export const submitReport = ({ dispatch, state }, context) => {
  dispatch(types.REPORT_CLEAR_ERRORS)
  dispatch(types.BUTTON_SUBMIT_LOADING, true)

  context.$http.post('report/', state.report.request).then(
    (response) => {
      dispatch(types.BUTTON_SUBMIT_LOADING, false)
      dispatch(types.USER_UPDATE_REPORTS, response.data)
      state.route.path = '/profile'
    },
    (response) => {
      for (var key in response.data) {
        switch (key) {
          case 'school':
            dispatch(types.REPORT_SHOW_ERROR, 'school', response.data[key])
          break;
          case 'category':
            dispatch(types.REPORT_SHOW_ERROR, 'category', response.data[key])
          break;
          case 'text':
            dispatch(types.REPORT_SHOW_ERROR, 'text', response.data[key])
          break;
          default:
            dispatch(types.REPORT_SHOW_ERROR, 'other', response.data[key])
        }
      }
      dispatch(types.BUTTON_SUBMIT_LOADING, false)
    }
  )
}

export const upvoteReport = ({ dispatch, state }, context) => {
  const endpoint = state.report.view.did_upvote ? 'unvote' : 'upvote'
  let data = {
    report_id: state.report.view.id,
    user_id: state.user.id
  }

  dispatch(types.REPORT_UPVOTE_LOADING, true)
  context.$http.post('report/' + endpoint, data).then(
    (response) => {
      dispatch(types.REPORT_UPDATE_UPVOTES, response.data.upvotes)
      dispatch(types.USER_UPDATE_UPVOTED, endpoint, state.report.view)
      dispatch(types.REPORT_UPVOTE_LOADING, false)
    },
    (response) => {
      console.log('Failed to ' + endpoint + ' report.')
    }
  )
}

export const followReport = ({ dispatch, state }, context) => {
  const endpoint = state.report.view.did_follow ? 'unfollow' : 'follow'
  let data = {
    report_id: state.report.view.id,
    user_id: state.user.id
  }

  dispatch(types.REPORT_FOLLOW_LOADING, true)
  context.$http.post('report/' + endpoint, data).then(
    (response) => {
      dispatch(types.REPORT_UPDATE_FOLLOW)
      dispatch(types.USER_UPDATE_FOLLOWING, endpoint, state.report.view)
      dispatch(types.REPORT_FOLLOW_LOADING, false)
    },
    (response) => {
      console.log('Failed to ' + endpoint)
    }
  )
}
