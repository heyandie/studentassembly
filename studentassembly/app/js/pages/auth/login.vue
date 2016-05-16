<template lang="jade">
section.page__wrapper.page--min-height
  .content__wrapper.content--small
    .content__section
      .alert__wrapper.alert--success(v-if="success.register")
        p {{ success.register }}
      .alert__wrapper.alert--success(v-if="success.resendVerification")
        p {{ success.resendVerification }}
      .alert__wrapper.alert--success(v-if="success.verifyAccount")
        p {{ success.verifyAccount }}
      .alert__wrapper.alert--success(v-if="success.resetPassword")
        p {{ success.resetPassword }}

      .alert__wrapper.alert--error(v-if="$route.query.s === 'expired'")
        p You have been inactive for 24 hours. For security measures, please log in again.
      .alert__wrapper.alert--error(v-if="error.other")
        p {{ error.other }}
      .alert__wrapper.alert--error(v-if="error.verify")
        p
          | {{ error.verify }}&nbsp;
          a(href="#0", @click.prevent="resendVerification(this)") Resend verification
          |.

      h2 Log in
      .form__wrapper
        form(@submit.prevent="login(this)")
          .form__element(:class="error.email ? 'form--empty' : ''")
            .form__label Email
            input(
              type="email",
              name="email",
              placeholder="juan@student.ph",
              autofocus="true",
              :value="user.email",
              :disabled="loading",
              @input="updateEmail"
            )
            .form__error(v-if="error.email")
              span {{ error.email }}
          .form__element(:class="error.password ? 'form--empty' : ''")
            .form__note.u-fl-r.u-mg-t-0
              a(v-link="{ name: 'reset-password' }") Forgot your password?
            .form__label Password
            input(
              type="password",
              name="password",
              placeholder="••••••••",
              :value="user.password",
              :disabled="loading",
              @input="updatePassword"
            )
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
import { login, resendVerification } from '../../vuex/actions/auth'

export default {
  vuex: {
    getters: {
      user: ({ auth }) => auth.user,
      error: ({ auth }) => auth.error,
      success: ({ auth }) => auth.success,
      loading: ({ auth }) => auth.buttonLoading
    },
    actions: {
      login,
      resendVerification,
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
  detached () {
    this.clearForm()
  },
  components: {
    'v-spinner': Spinner
  }
}
</script>
