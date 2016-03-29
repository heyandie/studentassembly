<template lang="jade">
v-header
section.page__wrapper
  .content__wrapper
    .content__section
      h1 Hello, {{ username }}!
      h3 Your Reports
      article.content__main
        .cards__wrapper
          a.card(v-for="report in reports" v-link="{ name: 'report-view', params: { id: report.id } }")
            strong {{ report.category }}
            br
            small at {{ report.school }}
            br
            | {{ report.text | truncate }}
      aside.content__secondary
</template>

<script>
import Header from '../../components/header.vue'
import Footer from '../../components/footer.vue'
import Spinner from '../../components/spinner.vue'

import { getProfile, getReports } from '../../vuex/actions/user'

export default {
  vuex: {
    getters: {
      username: ({ user }) => user.username,
      reports: ({ user }) => user.reports
    },
    actions: {
      getProfile,
      getReports
    }
  },
  created () {
    this.getProfile()
    this.getReports(this)

    // this.$http.get('report/' + this.reports[0].id).then(
    //   function(response) {
    //     console.log(response.data)
    //   },
    //   function(response) {
    //
    //   }
    // )
  },
  filters: {
    truncate (string) {
      if (string.length > 90)
        return string.substring(0, 90) + '...'
      else
        return string
    }
  },
  components: {
    'v-header': Header,
    'v-footer': Footer,
    'v-spinner': Spinner
  }
}
</script>
