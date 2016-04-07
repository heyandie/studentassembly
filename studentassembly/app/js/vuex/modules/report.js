import {
  BUTTON_SUBMIT_LOADING,
  REPORT_CLEAR_FIELDS,
  REPORT_RECEIVE_SCHOOLS,
  REPORT_RECEIVE_CATEGORIES,
  REPORT_UPDATE_QUESTIONS,
  REPORT_UPDATE_ANSWER,
  REPORT_UPDATE_REPORT_FIELD,
  REPORT_UPDATE_CONTACT_FIELD,
  REPORT_UPDATE_ATTACHMENT,
  REPORT_SHOW_ERROR,
  REPORT_RECEIVE_ID,
  REPORT_RECEIVE_REPORT
} from '../mutation-types'

const state = {
  buttonLoading: false,
  schools: [],
  categories: [],
  questions: [],
  error: {
    school: null,
    category: null,
    text: null,
    attachment: null
  },
  request: {
    contact: {
      allow_contact: 0,
      name: null,
      contact_number: null
    },
    report: {
      category: null,
      school: null,
      text: null,
      answers: [],
      files: [],
      allow_publish: 0
    }
  },
  view: null
}

const mutations = {
  [REPORT_CLEAR_FIELDS] (state) {
    state.buttonLoading = false
    state.schools = []
    state.categories = []
    state.questions = []

    state.request.contact = {
      allow_contact: 0,
      name: null,
      contact_number: null
    }
    state.request.report = {
      category: null,
      school: null,
      text: null,
      answers: [],
      files: [],
      allow_publish: 0
    }
  },

  [REPORT_RECEIVE_SCHOOLS] (state, schools) {
    state.schools = schools
  },

  [REPORT_RECEIVE_CATEGORIES] (state, categories) {
    state.categories = categories
  },

  [REPORT_UPDATE_QUESTIONS] (state) {
    state.questions = JSON.parse(state.categories[state.request.report.category - 1].questions)

    for (let i = 0; i < state.questions.length; i++) {
      state.request.report.answers.$set(i, {
        id: state.questions[i].id,
        text: ''
      })
    }
  },

  [REPORT_UPDATE_ANSWER] (state, index, value) {
    state.request.report.answers[index].text = value
  },

  [REPORT_UPDATE_REPORT_FIELD] (state, field, value) {
    state.request.report[field] = value
  },

  [REPORT_UPDATE_CONTACT_FIELD] (state, field, value) {
    state.request.contact[field] = value
  },

  [REPORT_UPDATE_ATTACHMENT] (state, index, attachment) {
    state.request.report.files.$set(index, attachment)
  },

  [REPORT_SHOW_ERROR] (state, type, message) {
    state.error[type] = message
  },

  [BUTTON_SUBMIT_LOADING] (state, buttonLoading) {
    state.buttonLoading = buttonLoading
  },

  [REPORT_RECEIVE_ID] (state, reportId) {
    state.view = {
      id: reportId
    }
  },

  [REPORT_RECEIVE_REPORT] (state, report) {
    state.view = report
    state.view.questions = JSON.parse(report.questions)
  }
}

export default {
  state,
  mutations
}
