<template lang="jade">
v-header
section.page__wrapper
  .content__wrapper.content--small
    .content__section
      .form__wrapper
        h2 {{ msg }}
        form
          .form__element
            input(type="email" v-model="user.email" placeholder="Email")
            .form__error
              span(v-if="emailTaken") This email is already taken.
          .form__element.form--empty
            input(type="password" v-model="user.password" placeholder="Password")
            .form__error
              span(v-if="passwordShort") Your password should at least be 8 characters long.
          .form__element
            input(type="password" v-model="user.repeatPassword" placeholder="Repeat password")
            .form__error
              span(v-if="passwordsMismatch") Oops, the passwords did not match.
          .form__element
            button(type="submit" @click.prevent="register") Register
</template>

<script>
var Header = require('../components/header.vue');

module.exports = {
  data: function() {
    return {
      msg: 'Create an account',
      user: {
        email: null,
        password: null,
        repeatPassword: null
      },
      emailTaken: true,
      passwordShort: true,
      passwordsMismatch: true
    }
  },
  methods: {
    validateInput: function() {

    },
    sendRequest: function() {
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
    },
    register: function() {
      validateInput();
      sendRequest();
    }
  },
  components: {
    'v-header': Header
  }
}
</script>
