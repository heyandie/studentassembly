import {
  REPORT_RECEIVE_SCHOOLS,
  REPORT_RECEIVE_CATEGORIES
} from '../mutation-types'

const state = {
  buttonLoading: false,
  schools: [],
  categories: [],
  request: {
    contact: {
      allow_contact: false,
      name: null,
      contact_number: null
    },
    report: {
      category: null,
      school: null,
      text: null,
      answers: null,
      files: [null, null, null],
      allow_publish: false
    }
  }
}

const mutations = {
  [REPORT_RECEIVE_SCHOOLS] (state, schools) {
    state.schools = schools
  },

  [REPORT_RECEIVE_CATEGORIES] (state, categories) {
    state.categories = categories
  }
}

export default {
  state,
  mutations
}
