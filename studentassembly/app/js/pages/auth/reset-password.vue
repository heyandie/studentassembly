<template lang="jade">
section.page__wrapper.page--min-height
  .content__wrapper.content--small
    .content__section
      .alert__wrapper.alert--success(v-if="success.sendResetPasswordLink")
        p {{ success.sendResetPasswordLink }}

      .alert__wrapper.alert--error(v-if="error.other")
        p {{ error.other }}

      template(v-if="receivedLink")
        h2 Enter your new password
        .form__wrapper
          form(@submit.prevent="resetPassword(this)")
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
              button(type="submit", :disabled="loading")
                span(v-show="!loading") Reset password
                v-spinner(v-show="loading", :on-button="true", color="#fff", radius="7")
      template(v-else)
        h2 Reset your password
        .form__wrapper
          form(@submit.prevent="sendResetPasswordLink(this)")
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
            .form__element
              button(type="submit", :disabled="loading")
                span(v-show="!loading") Send reset link
                v-spinner(v-show="loading", :on-button="true", color="#fff", radius="7")
</template>

<script>
import Spinner from '../../components/spinner.vue'
import { sendResetPasswordLink, resetPassword } from '../../vuex/actions/auth'

export default {
  vuex: {
    getters: {
      user: ({ auth }) => auth.user,
      error: ({ auth }) => auth.error,
      success: ({ auth }) => auth.success,
      loading: ({ auth }) => auth.buttonLoading,
      passwordVisible: ({ auth }) => auth.passwordVisible
    },
    actions: {
      sendResetPasswordLink,
      resetPassword,
      updateEmail: ({ dispatch }, e) => {
        dispatch('AUTH_UPDATE_FIELD', 'email', e.target.value)
      },
      updatePassword: ({ dispatch }, e) => {
        dispatch('AUTH_UPDATE_FIELD', 'password', e.target.value)
      },
      togglePassword: ({ dispatch }) => {
        dispatch('AUTH_TOGGLE_PASSWORD')
      },
      clearForm: ({ dispatch }) => {
        dispatch('AUTH_CLEAR_FIELDS')
        dispatch('AUTH_CLEAR_ERRORS')
      }
    }
  },
  computed: {
    receivedLink () {
      return this.$route.query.token && this.$route.query.token.split('.').length === 2
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
