<template lang="jade">
section.page__wrapper.page--min-height
  .content__wrapper.content--small
    .content__section
      .alert__wrapper.alert--success(v-if="registerSuccess")
        h3 Verify your email
        p
          | We've sent a link to your email address so we can verify you. After doing so, you can start&nbsp;
          a(v-link="{ name: 'login' }") logging in.
      h2 Create an account
      .form__wrapper
        form(@submit.prevent="register(this)")
          .form__element(:class="error.email ? 'form--empty' : ''")
            .form__label Email
            input(type="email", name="email", placeholder="University email is highly discouraged.", autofocus="true", :value="user.email", @input="updateEmail")
            .form__error(v-if="error.email")
              span {{ error.email }}
          .form__element(:class="error.password || error.passwordRepeat ? 'form--empty' : ''")
            .form__label Password
            input(type="password", name="password", placeholder="Must be at least 8 characters long.", :value="user.password", @input="updatePassword")
            .form__error(v-if="error.password")
              span {{ error.password }}
          .form__element(:class="error.passwordRepeat ? 'form--empty' : ''")
            .form__label Repeat password
            input(type="password", name="passwordRepeat", placeholder="Just to be sure.", :value="user.passwordRepeat", @input="updatePasswordRepeat")
            .form__error(v-if="error.passwordRepeat")
              span {{ error.passwordRepeat }}
          .form__element
            .form__checkbox
              input(type="checkbox", name="agree_terms", id="agree_terms", :checked="termsAgree", @change="toggleTerms")
              label(for="agree_terms")
                | I agree with the&nbsp;
                a(href="#0") Terms of Service.
            .form__error(v-if="error.termsAgree")
              span {{ error.termsAgree }}
          .form__element
            button(type="submit", :disabled="loading")
              span(v-show="!loading") Register
              v-spinner(v-show="loading", :on-button="true", color="#fff", radius="7")
      p.small
        | Already have an account?&nbsp;
        a(v-link="{ name: 'login' }") Log in.
</template>

<script>
import Spinner from '../../components/spinner.vue'
import { register } from '../../vuex/actions/auth'

export default {
  vuex: {
    getters: {
      user: ({ auth }) => auth.user,
      error: ({ auth }) => auth.error,
      loading: ({ auth }) => auth.buttonLoading,
      termsAgree: ({ auth }) => auth.termsAgree,
      registerSuccess: ({ auth }) => auth.registerSuccess
    },
    actions: {
      register,
      updateEmail: ({ dispatch }, e) => {
        dispatch('AUTH_UPDATE_FIELD', 'email', e.target.value)
      },
      updatePassword: ({ dispatch }, e) => {
        dispatch('AUTH_UPDATE_FIELD', 'password', e.target.value)
      },
      updatePasswordRepeat: ({ dispatch }, e) => {
        dispatch('AUTH_UPDATE_FIELD', 'passwordRepeat', e.target.value)
      },
      toggleTerms: ({ dispatch }, e) => {
        dispatch('AUTH_CHECK_TERMS', e.target.checked)
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
