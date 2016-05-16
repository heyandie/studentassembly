<template lang="jade">
section.page__wrapper.page--min-height
  .content__wrapper.content--small
    .content__section
      h2 Create an account
      .form__wrapper
        form(@submit.prevent="register(this)")
          .form__element(:class="error.email ? 'form--empty' : ''")
            .form__label Email
            input(
              type="email",
              name="email",
              placeholder="School email is highly discouraged.",
              autofocus="true",
              :value="user.email",
              :disabled="loading",
              @input="updateEmail"
            )
            .form__error(v-if="error.email")
              span {{ error.email }}
          .form__element(:class="error.password || error.passwordRepeat ? 'form--empty' : ''")
            .form__label Password
            input(
              :type="passwordVisible ? 'text' : 'password'",
              name="password",
              placeholder="Must be at least 8 characters long.",
              :value="user.password",
              :disabled="loading",
              @input="updatePassword"
            )
            .form__visible-toggle(
              @click="togglePassword",
              :class="passwordVisible ? 'form__visible-toggle--on' : ''"
            )
            .form__error(v-if="error.password")
              span {{ error.password }}
          .form__element
            .form__checkbox
              input(
                type="checkbox",
                name="agree_terms",
                id="agree_terms",
                :checked="user.agreeTerms",
                :disabled="loading",
                @change="toggleAgreeTerms"
              )
              label(for="agree_terms")
                | I agree with the&nbsp;
                a(href="#0") Terms of Service.
            .form__error(v-if="error.agreeTerms")
              span {{ error.agreeTerms }}
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
      passwordVisible: ({ auth }) => auth.passwordVisible
    },
    actions: {
      register,
      updateEmail: ({ dispatch }, e) => {
        dispatch('AUTH_UPDATE_FIELD', 'email', e.target.value)
      },
      updatePassword: ({ dispatch }, e) => {
        dispatch('AUTH_UPDATE_FIELD', 'password', e.target.value)
      },
      togglePassword: ({ dispatch }) => {
        dispatch('AUTH_TOGGLE_PASSWORD')
      },
      toggleAgreeTerms: ({ dispatch }, e) => {
        dispatch('AUTH_UPDATE_FIELD', 'agreeTerms', e.target.checked)
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
