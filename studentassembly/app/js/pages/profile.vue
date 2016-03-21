<template lang="jade">
v-header
section.page__wrapper
  .content__wrapper
    .content__section
      h1 Profile
      h3 Hello, {{ username }}!
      ul
        li(v-for="report in reports")
          p
            strong {{ report.category }}
            br
            small at {{ report.school }}
            br
            | {{ report.text }}
</template>

<script>
import Header from '../components/header.vue'
import Footer from '../components/footer.vue'
import Spinner from '../components/spinner.vue'

import { getReports } from '../vuex/actions/user'

export default {
  vuex: {
    getters: {
      username: ({ user }) => user.username,
      reports: ({ user }) => user.reports
    },
    actions: {
      getReports
    }
  },
  created () {
    this.getReports(this)
  },
  components: {
    'v-header': Header,
    'v-footer': Footer,
    'v-spinner': Spinner
  }
}
</script>
