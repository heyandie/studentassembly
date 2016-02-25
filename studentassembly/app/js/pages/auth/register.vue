<template lang="jade">
v-header
section.page__wrapper
  .content__wrapper.content--small
    .content__section
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
            input(type="password" v-model="user.repeatPassword" placeholder="Repeat password")
            .form__error
              span(v-if="passwordsMismatch") Oops, the passwords did not match.
          .form__element
            button(type="submit" @click.prevent="register" v-bind:disabled="loading")
              span(v-show="!loading") Register
              .button__spinner(v-show="loading")
                v-spinner(color="#fff" height="6px" width="3px" radius="8px")
</template>

<script>
var Header = require('../../components/header.vue');
var Spinner = require('../../elements/spinner.vue');

module.exports = {
  data: function() {
    return {
      msg: 'Create an account',
      user: {
        email: null,
        password: null,
        repeatPassword: null
      },
      emailError: null,
      passwordError: null,
      passwordsMismatch: false,
      loading: false
    }
  },
  methods: {
    clearErrors: function() {
      this.emailError = null;
      this.passwordError = null;
      this.passwordsMismatch = false;
    },
    validateInput: function() {
      this.clearErrors();

      if (this.user.password !== this.user.repeatPassword) {
        this.passwordsMismatch = true;
        return false;
      }

      return true;
    },
    sendRequest: function() {
      var that = this;
      that.loading = true;
      client({ path: 'register', entity: this.user }).then(
        function (response) {
          that.$route.router.go({ name: 'login' });
        },
        function (response) {
          if (response.status && response.status.code === 400) {
            for (var key in response.entity) {
              if (key === 'email') {
                try {
                  that.emailError = response.entity[key];
                } catch(e) {
                  console.log(e);
                }
              }

              if (key === 'password') {
                try {
                  that.passwordError = response.entity[key];
                } catch(e) {
                  console.log(e);
                }
              }
            }
          }
          that.loading = false;
        }
      );
    },
    register: function() {
      if (this.validateInput())
        this.sendRequest();
    }
  },
  components: {
    'v-header': Header,
    'v-spinner': Spinner
  }
}
</script>
