import {
  STAFF_RECEIVE_ALL,
  STAFF_UPDATE_SEARCHKEY,
  STAFF_UPDATE_SORT
} from '../mutation-types'

const state = {
  all: [],
  params: ['name', 'school', 'rating_-_overall'],
  searchKey: '',
  sortKey: 'rating_-_overall',
  order: -1
}

const mutations = {
  [STAFF_RECEIVE_ALL] (state, staff) {
    staff.forEach((mem) => {
      Object.defineProperty(mem, 'rating_-_overall', {
        get () { return this.rating.overall }
      })
    })
    state.all = staff
  },

  [STAFF_UPDATE_SEARCHKEY] (state, searchKey) {
    state.searchKey = searchKey
  },

  [STAFF_UPDATE_SORT] (state, sortKey) {
    state.order = (state.sortKey === sortKey) ? state.order * -1 : 1
    state.sortKey = sortKey
  }
}

export default {
  state,
  mutations
}
