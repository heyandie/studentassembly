<template lang="jade">
section.page__wrapper.page--min-height
  .content__wrapper.content--small
    .content__section
      .alert__wrapper.alert--error(v-if="error.verify")
        h3 Oops!
        p
          | {{ error.verify }}&nbsp;
          a(v-link="{ name: 'login' }") Resend verification.
      .alert__wrapper.alert--success(v-if="$route.query.s === 'verified'")
        h3 Your account has been verified!
        p
          | Log in using your email and password to start using Student Assembly.
      .alert__wrapper.alert--error(v-if="$route.query.s === 'expired'")
        //- h3 Your account has been verified!
        p
          | You have been logged out due to inactivity. For security measures, please log in again.

      h2 Log in
      .form__wrapper
        form(@submit.prevent="login(this)")
          .form__element(:class="error.email ? 'form--empty' : ''")
            .form__label Email
            input(type="email", name="email", placeholder="juan@student.ph", autofocus="true", :value="user.email", @input="updateEmail")
            .form__error(v-if="error.email")
              span {{ error.email }}
          .form__element(:class="error.password ? 'form--empty' : ''")
            .form__note.pull-right.u-mg-t-0
              a(v-link="{ name: 'login' }") Forgot your password?
            .form__label Password
            input(type="password", name="password", placeholder="••••••••", :value="user.password", @input="updatePassword")
            .form__error(v-if="error.password")
              span {{ error.password }}
          .form__element
            button(type="submit", :disabled="loading")
              span(v-show="!loading") Login
              v-spinner(v-show="loading", :on-button="true", color="#fff", radius="7")
      p.small
        | Don't have an account yet?&nbsp;
        a(v-link="{ name: 'register' }") Create one.
</template>

<script>
import Spinner from '../../components/spinner.vue'

import { login } from '../../vuex/actions/auth'

export default {
  vuex: {
    getters: {
      user: ({ auth }) => auth.user,
      error: ({ auth }) => auth.error,
      loading: ({ auth }) => auth.buttonLoading
    },
    actions: {
      login,
      updateEmail: ({ dispatch }, e) => {
        dispatch('AUTH_UPDATE_FIELD', 'email', e.target.value)
      },
      updatePassword: ({ dispatch }, e) => {
        dispatch('AUTH_UPDATE_FIELD', 'password', e.target.value)
      },
      clearForm: ({ dispatch }) => {
        dispatch('AUTH_CLEAR_ERRORS')
        dispatch('AUTH_CLEAR_FIELDS')
      }
    }
  },
  created () {
    this.clearForm()
  },
  components: {
    'v-spinner': Spinner
  }
}
</script>
