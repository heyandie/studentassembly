<template lang="jade">
section.page__wrapper
  .content__wrapper
    .content__section
      article.content__main
        .form__wrapper
          .spinner__wrapper(v-if="loading")
            v-spinner
          template(v-if="!loading")
            h3
              .pull-right
                small.list__item-remark(:class="report.is_approved ? 'list__item--approved' : 'list__item--not-approved'") {{ report.is_approved ? 'Approved' : 'Not Approved' }}
              span {{ report.category }}
            h4 {{ report.school }}
            p {{ report.text }}
            template(v-if="report.files.length")
              hr
              h5 Attachments
              .list__item-attachment(v-for="file in report.files")
                a(target="_blank" v-bind:href="file.blob" v-bind:download="file.name")
                  .list__item-attachment-preview(v-bind:style="{ backgroundImage: 'url(' + file.blob + ')' }")
                  span {{ file.name }}
</template>

<script>
import Spinner from '../../components/spinner.vue'
import { getReport } from '../../vuex/actions/report'

export default {
  vuex: {
    getters: {
      report: ({ report }) => report.view,
      loading: ({ report }) => report.buttonLoading
    },
    actions: {
      getReport,
      getID: ({ dispatch, state }) => {
        dispatch('REPORT_CLEAR_VIEW')
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
