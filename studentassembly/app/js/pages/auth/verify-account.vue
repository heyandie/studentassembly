<template lang="jade">
section.page__wrapper.page--min-height
  .content__wrapper.content--small
    .content__section
      .form__wrapper
        .spinner__wrapper
          v-spinner
          h4 Verifying your account...
</template>

<script>
import Spinner from '../../components/spinner.vue'
import { verifyAccount } from '../../vuex/actions/auth'

export default {
  vuex: {
    actions: {
      verifyAccount
    }
  },
  route: {
    activate () {
      this.verifyAccount(this, this.$route.params.token)
    }
  },
  components: {
    'v-spinner': Spinner
  }
}
</script>
