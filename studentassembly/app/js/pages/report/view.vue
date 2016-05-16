<template lang="jade">
section.page__wrapper.page--light
  .content__wrapper
    .content__section
      article.content__main
        .spinner__wrapper(v-if="$loadingRouteData")
          v-spinner
          h4 Loading report...
        template(v-if="!$loadingRouteData")
          .paragraph__section
            .button__group.u-fl-r
              a.button.button--tiny.button--light(href="#0", @click.prevent="upvoteReport(this)", :disabled="report.upvoteLoading")
                span(v-show="!report.upvoteLoading")
                  span(:class="!report.did_upvote ? 'button--tiny-header' : ''") {{ report.did_upvote ? 'Upvoted' : 'Upvote' }}
                  span.button--tiny-number {{ report.upvotes }}
                v-spinner(v-show="report.upvoteLoading", :on-button="true", color="#999", radius="7")
              a.button.button--tiny.button--simple(href="#0", @click.prevent="followReport(this)", :disabled="following")
                span(v-show="!following") {{ report.did_follow ? 'Unfollow' : 'Follow' }}
                v-spinner(v-show="following", :on-button="true", color="#999", radius="7")
              v-share-button(type="report", :type-id="report.id")
            h2 {{ report.category }}
            h3.u-mg-b-24
              span.header--light {{ report.school }}
              small.list__item-remark.u-mg-t-8(
                :class="report.is_approved ? 'list__item--approved' : 'list__item--not-approved'"
              )
                span {{ report.status }}
                span.list__item-date &nbsp;as of {{ report.updated_at | toDateString }}, reported by {{ report.alias }}
            hr
          .paragraph__section(v-for="(index, question) in report.questions")
            h3 {{ question.text }}
            p {{ report.answers[index].text }}
          .paragraph__section
            h3 Details
            p {{{ report.text | nl2br }}}
          .paragraph__section(v-if="report.files")
            h3 Attachments
            .u-cf
              .list__item-attachment(v-for="file in report.files")
                a(target="_blank" v-bind:href="file.blob" v-bind:download="file.name")
                  .list__item-attachment-preview(v-bind:style="{ backgroundImage: 'url(' + file.blob + ')' }")
                  span {{ file.name }}
      aside.content__secondary.content--additional-info
        h4 Other reports in this school
        template(v-if="!$loadingRouteData")
          .u-mg-t-24(v-for="related in report.related")
            a(v-link="{ name: 'report-view', params: { id: related.id }}")
              h5 {{ related.category }}
              p.small {{ related.text | truncate 72 }}
          .u-mg-t-12(v-if="!report.related.length")
            p.small There are no related reports.
            a.button.button--mini.button--hollow(
              v-link="{ name: 'file-a-report', query: { school: report.school }}"
            ) File a report

section.page__wrapper(:class="$loadingRouteData ? 'page--min-height' : ''")
  .content__wrapper
    .content__section
      template(v-if="!$loadingRouteData")
        .content__half
          h4 {{ report.school }}
          hr.small
          p.small 400 reports
          p.small 224 resolved cases
          p.small Most reported category &mdash; Policies
          p.small Average staff rating (overall) &mdash; 3 / 5
          a.button.button--tiny.button--inverted(
            v-link="{ name: 'file-a-report', query: { school: report.school }}"
          ) File a report
          a.button.button--tiny.button--inverted(
            v-link="{ name: 'rate', query: { school: report.school }}"
          ) Rate their staff
        .content__half
          .u-div-240.u-google-map
            iframe(
              :src="googleMap",
              width="100%",
              height="600",
              frameborder="0",
              style="border:0",
              allowfullscreen
            )
</template>

<script>
import Spinner from '../../components/spinner.vue'
import ShareButton from '../../components/share-button.vue'
import { getReport, getRelatedReports, upvoteReport, followReport } from '../../vuex/actions/report'

export default {
  vuex: {
    getters: {
      userID: ({ user }) => user.id,
      report: ({ report }) => report.view
    },
    actions: {
      getReport,
      getRelatedReports,
      upvoteReport,
      followReport
    }
  },
  route: {
    data (transition) {
      return this.getReport(this)
    }
  },
  computed: {
    googleMap () {
      return 'https://www.google.com/maps?q='
        + encodeURIComponent(this.report.school)
        + '&z=15&output=embed'
    }
  },
  watch: {
    'report': function (val, oldVal) {
      if (typeof val.category !== 'undefined')
        this.getRelatedReports(this)
    }
  },
  components: {
    'v-spinner': Spinner,
    'v-share-button': ShareButton
  }
}
</script>
