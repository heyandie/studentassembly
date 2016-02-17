<template lang="jade">
v-header
section.page__wrapper
  .content__wrapper
    .content__section
      h1 {{ msg }}
      form
        input(type="email" v-model="user.email" placeholder="Email")
        input(type="password" v-model="user.password" placeholder="Password")
        button(type="submit" @click.prevent="attemptLogin") Login
</template>

<script>
var Header = require('../components/header.vue');

module.exports = {
  data: function() {
    return {
      msg: 'Login',
      user: {
        email: null,
        password: null
      }
    }
  },
  methods: {
    attemptLogin: function() {
      console.log('yay');
    }
  },
  components: {
    'v-header': Header
  }
}
</script>
