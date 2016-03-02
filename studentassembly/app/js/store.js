import Vuex from 'vuex'
import Vue from 'vue'

Vue.use(Vuex);

module.exports = new Vuex.Store({
  state: {
    token: null
  },
  mutations: {
    SET_LOGIN (state, token) {
      state.token = token;
    },
    SET_LOGOUT (state) {
      state.token = null;
    }
  }
});
