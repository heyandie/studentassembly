<template lang="jade">
v-header
section.page__wrapper
  .content__wrapper.content--small
    .content__section
      h1(v-if="loggedInMessage") {{ loggedInMessage }}
      .form__wrapper
        h2 {{ msg }}
        form
          .form__element(:class="emailError ? 'form--empty' : ''")
            input(type="email" v-model="user.email" placeholder="Email")
            .form__error
              span {{ emailError }}
          .form__element(:class="passwordError ? 'form--empty' : ''")
            input(type="password" v-model="user.password" placeholder="Password")
            .form__error
              span {{ passwordError }}
          .form__element
            button(type="submit" @click.prevent="login") Login
</template>

<script>
var Header = require('../components/header.vue');
var Store = require('../store');

module.exports = {
  data: function() {
    return {
      msg: 'Login to StudentAssembly',
      user: {
        email: null,
        password: null
      },
      emailError: null,
      passwordError: null,
      loggedInMessage: null
    }
  },
  methods: {
    clearErrors: function() {
      this.emailError = null;
      this.passwordError = null;
    },
    validateInput: function() {
      this.clearErrors();
      return true;
    },
    sendRequest: function() {
      var that = this;
      client({ path: 'token-auth', entity: this.user }).then(
        function (response) {
          that.loggedInMessage = "You are logged in.";
        },
        function (response) {
          console.log(response);
          if (response.status && response.status.code === 400) {
            for (var key in response.entity) {
              if (key === 'non_field_errors') {
                try {
                  that.emailError = response.entity[key];
                  that.passwordError = response.entity[key];
                } catch(e) {
                  console.log(e);
                }
              }
            }
          }
        }
      );
    },
    login: function() {
      if (this.validateInput())
        this.sendRequest();
    }
  },
  components: {
    'v-header': Header
  }
}
</script>
