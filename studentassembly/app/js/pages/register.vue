<template lang="jade">
v-header
section.page__wrapper
  .content__wrapper
    .content__section
      h1 {{ msg }}
      form
        input(type="email" v-model="user.email" placeholder="Email")
        input(type="password" v-model="user.password" placeholder="Password")
        button(type="submit" @click.prevent="register") Register
</template>

<script>
var Header = require('../components/header.vue');

module.exports = {
  data: function() {
    return {
      msg: 'Register',
      user: {
        email: null,
        password: null
      }
    }
  },
  methods: {
    register: function() {
      var that = this;
      client({ path: 'register', entity: this.user }).then(
        function (response) {
          // that.$dispatch('userHasFetchedToken', response.entity.token);
          // that.getUserData();
          console.log('success', response);
        },
        function (response) {
          that.messages = [];
          console.log('fail', response);
          if (response.status && response.status.code === 401)
            that.messages.push({type: 'danger', message: 'Sorry, you provided invalid credentials'});
        }
      );
    }
  },
  components: {
    'v-header': Header
  }
}
</script>
