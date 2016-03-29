<template lang="jade">
v-header
section.page__wrapper
  .content__wrapper
    .content__section
      h2 Hello, {{ username }}!
      article.content__main
        h3 Your Reports
        .list__group
          .spinner__wrapper(v-if="loading")
            v-spinner
          template(v-if="!loading")
            a.list__item(v-for="report in reports" v-link="{ name: 'report-view', params: { id: report.id } }")
              h4
                .pull-right
                  small.list__item-remark(:class="report.is_approved ? 'list__item--approved' : 'list__item--not-approved'") {{ report.is_approved ? 'Approved' : 'Not Approved' }}
                span {{ report.category }}
                br
                small {{ report.school }}
              p {{ report.text | truncate }}
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
      reports: ({ user }) => user.reports,
      loading: ({ report }) => report.buttonLoading
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
      if (string.length > 140)
        return string.substring(0, 140) + '...'
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
