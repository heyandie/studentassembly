// Vuex is an ES6 module
import Vuex from 'vuex';

// Vue
var Vue = require('vue');

Vue.use(Vuex);

module.exports = new Vuex.Store({
  state: {
    counter: 0
  },
  mutations: {
    INCREMENT (state) {
      state.counter++;
    }
  }
});
