<template lang="jade">
v-header
section.page__wrapper
  .content__wrapper.content--small
    .content__section
      .alert__wrapper.alert--success(v-if="registerSuccess")
        h3 Verify your email
        p
          | We've sent a link to your email address so we can verify you. After doing so, you can start&nbsp;
          a(v-link="{ name: 'login' }") logging in.
      h2 Create an account
      .form__wrapper
        form
          .form__element(:class="error.email ? 'form--empty' : ''")
            .form__label Email
            input(type="email" name="email" placeholder="University email is highly discouraged." v-bind:value="user.email" @input="updateEmail")
            .form__error(v-if="error.email")
              span {{ error.email }}
          .form__element(:class="error.password || error.passwordRepeat ? 'form--empty' : ''")
            .form__label Password
            input(type="password" name="password" placeholder="Must be at least 8 characters long." v-bind:value="user.password" @input="updatePassword")
            .form__error(v-if="error.password")
              span {{ error.password }}
          .form__element(:class="error.passwordRepeat ? 'form--empty' : ''")
            .form__label Repeat password
            input(type="password" name="passwordRepeat" placeholder="Just to be sure." v-bind:value="user.passwordRepeat" @input="updatePasswordRepeat")
            .form__error(v-if="error.passwordRepeat")
              span {{ error.passwordRepeat }}
          .form__element
            .form__checkbox
              input(type="checkbox" name="agree_terms" id="agree_terms" v-bind:checked="termsAgree" @change="toggleTerms")
              label(for="agree_terms")
                | I agree with the&nbsp;
                a(href="#0") Terms of Service.
            .form__error(v-if="error.termsAgree")
              span {{ error.termsAgree }}
          .form__element
            button(type="submit" @click.prevent="register(this)" v-bind:disabled="loading")
              span(v-show="!loading") Register
              .button__spinner(v-show="loading")
                v-spinner(color="#fff" height="6px" width="3px" radius="8px")
      p.small
        | Already have an account?&nbsp;
        a(v-link="{ name: 'login' }") Log in.

</template>

<script>
import Header from '../../components/header.vue'
import Footer from '../../components/footer.vue'
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
  ready () {
    this.clearForm()
  },
  components: {
    'v-header': Header,
    'v-footer': Footer,
    'v-spinner': Spinner
  }
}
</script>
