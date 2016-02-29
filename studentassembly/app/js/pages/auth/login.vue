<template lang="jade">
v-header
section.page__wrapper
  .content__wrapper.content--small
    .content__section
      router-view
      .form__wrapper
        h2 Login to StudentAssembly
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
            button(type="submit" @click.prevent="login" v-bind:disabled="loading")
              span(v-show="!loading") Login
              .button__spinner(v-show="loading")
                v-spinner(color="#fff" height="6px" width="3px" radius="8px")
</template>

<script>
var Header = require('../../components/header.vue');
var Spinner = require('../../components/spinner.vue');
var Store = require('../../store');

module.exports = {
  data: function() {
    return {
      user: {
        email: null,
        password: null
      },
      emailError: null,
      passwordError: null,
      loading: false
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
      that.loading = true;
      client({ path: 'token_auth', entity: this.user }).then(
        function (response) {
          that.loading = false;
          that.$route.router.go('/profile');
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
          that.loading = false;
        }
      );
    },
    login: function() {
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
