<template lang="jade">
section.page__wrapper.page--min-height
  .content__wrapper
    .content__section
      article.content__main
        .form__wrapper(v-if="loading")
          .spinner__wrapper
            v-spinner
        template(v-if="!loading")
          //- .u-div-180
          //-   .u-bg-img.u-br-4(style="background-image:url('/static/img/schools/pup-manila.jpg');")
          .form__wrapper
            h3
              span {{ report.category }}
              br
              span.header--light {{ report.school }}
            small.list__item-remark(:class="report.is_approved ? 'list__item--approved' : 'list__item--not-approved'")
              strong {{ report.is_approved ? 'Approved' : 'Not Approved' }}
            small.list__item-date as of {{ report.updated_at | humanizeDate }}
            hr
            template(v-for="(index, question) in report.questions")
              h4 {{ question.text }}
              p {{ report.answers[index].text }}
            hr
            h4 Details
            p {{ report.text }}
            template(v-if="report.files.length")
              hr
              h4 Attachments
              .u-cf
                .list__item-attachment(v-for="file in report.files")
                  a(target="_blank" v-bind:href="file.blob" v-bind:download="file.name")
                    .list__item-attachment-preview(v-bind:style="{ backgroundImage: 'url(' + file.blob + ')' }")
                    span {{ file.name }}
          .button__group.button--on-hover
            .pull-left
              a.button.button--small(href="#0") Follow
            .pull-right
              a.button.button--small.button--facebook(target="_blank" href="#0")
                img.button__icon(src="/static/img/fb-logo-white.png" height="14")
                span Share
              a.button.button--small.button--twitter(target="_blank" href="https://twitter.com/intent/tweet?text=Share%20Report")
                img.button__icon(src="/static/img/twitter-logo-white.png" height="14")
                span Tweet

      aside.content__secondary.content--additional-info
        h4 Related reports

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
        dispatch('REPORT_RECEIVE_ID', state.route.params.id)
      }
    }
  },
  filters: {
    humanizeDate (date) {
      return new Date(date).toDateString()
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
