<template lang="jade">
v-header
section.page__wrapper
  .content__wrapper.content--small
    .content__section
      .alert__wrapper.alert--success(v-if="registered")
        h3 Verify your email
        p
          | We've sent a link to your email address so we can verify you. After doing so, you can start&nbsp;
          a(v-link="{ name: 'login' }") logging in.
      h2 Create an account
      .form__wrapper
        form
          .form__element(:class="emailError ? 'form--empty' : ''")
            .form__label Email
            input(type="email" name="email" v-model="user.email" placeholder="Use a valid email!")
            .form__error
              span {{ emailError }}
          .form__element(:class="passwordError ? 'form--empty' : ''")
            .form__label Password
            input(type="password" name="password" v-model="user.password" placeholder="Must be at least 8 characters long.")
            .form__error
              span {{ passwordError }}
          .form__element
            .form__label Repeat password
            input(type="password" name="repeatPassword" v-model="user.repeatPassword" placeholder="Just to be sure.")
            .form__error
              span(v-if="passwordsMismatch") Oops, the passwords did not match.
          .form__element
            .form__checkbox
              input(type="checkbox" name="agree_terms" id="agree_terms")
              label(for="agree_terms")
                | I agree with the&nbsp;
                a(href="#0") Terms of Service.
          .form__element
            button(type="submit" @click.prevent="register" v-bind:disabled="loading")
              span(v-show="!loading") Register
              .button__spinner(v-show="loading")
                v-spinner(color="#fff" height="6px" width="3px" radius="8px")
      p.small
        | Already have an account?&nbsp;
        a(v-link="{ name: 'login' }") Log in.
</template>

<script>
var Header = require('../../components/header.vue');
var Spinner = require('../../components/spinner.vue');

module.exports = {
  data: function() {
    return {
      user: {
        email: null,
        password: null,
        repeatPassword: null
      },
      emailError: null,
      passwordError: null,
      passwordsMismatch: false,
      registered: false,
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
          that.registered = true;
          that.loading = false;
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

          if (response.status) {

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


// Registration information
// Please enter a valid e-mail address. All e-mails from the system will be sent to this address. The e-mail address is not made public and will only be used if you wish to receive a new password or wish to receive certain news or notifications by e-mail.
// We aspire to make you feel as comfortable as possible using this website. We therefore do not ask for your name and do not require you to tell us your university or department. This enables you to remain as anonymous as possible. We also will assign you a random username so that the username is not personally linked to you. We require an email address simply to help us reduce fraud.
// For security reasons, we recommend that you do not use a university email address.
</script>
