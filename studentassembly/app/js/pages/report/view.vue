<template lang="jade">
section.page__wrapper
  .content__wrapper
    .content__section
      article.content__main
        h3 {{ report.category }}
        h4 {{ report.school }}
        p {{ report.text }}
        hr
        h5 Files
        a(v-for="file in report.files" target="_blank" v-bind:href="file.blob" v-bind:download="file.name") {{ file.name }}
      aside.content__secondary
</template>

<script>
import Spinner from '../../components/spinner.vue'
import { getReport } from '../../vuex/actions/report'

export default {
  vuex: {
    getters: {
      report: ({ report }) => report.view
    },
    actions: {
      getReport,
      getID: ({ dispatch, state }) => {
        dispatch('REPORT_RECEIVE_ID', state.route.params.id)
      }
    }
  },
  created () {
    this.getID()
    this.getReport(this)
  },
  components: {
    'v-spinner': Spinner
  }
}
</script>
