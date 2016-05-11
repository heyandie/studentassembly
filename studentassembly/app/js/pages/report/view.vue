<template lang="jade">
section.page__wrapper.page--light
  .content__wrapper
    .content__section
      article.content__main
        .spinner__wrapper(v-if="loading")
          v-spinner
          h4 Loading report...
        template(v-if="!loading")
          .paragraph__section
            .button__group.u-fl-r
              a.button.button--tiny.button--light(href="#0", @click.prevent="upvoteReport", :disabled="upvoting")
                span(v-show="!upvoting")
                  span(:class="!report.did_upvote ? 'button--tiny-header' : ''") {{ report.did_upvote ? 'Upvoted' : 'Upvote' }}
                  span.button--tiny-number {{ report.upvotes }}
                v-spinner(v-show="upvoting", :on-button="true", color="#999", radius="7")
              a.button.button--tiny.button--simple(href="#0", @click.prevent="followReport", :disabled="following")
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
            p(v-for="paragraph in detailText") {{ paragraph }}
          .paragraph__section(v-if="hasAttachments")
            h3 Attachments
            .u-cf
              .list__item-attachment(v-for="file in report.files")
                a(target="_blank" v-bind:href="file.blob" v-bind:download="file.name")
                  .list__item-attachment-preview(v-bind:style="{ backgroundImage: 'url(' + file.blob + ')' }")
                  span {{ file.name }}
      aside.content__secondary.content--additional-info
        h4 Other reports in this school
        template(v-if="relatedReports.length")
          .u-mg-t-24(v-for="related in relatedReports")
            a(v-link="{ name: 'report-view', params: { id: related.id }}")
              h5 {{ related.category }}
              p.small {{ related.text | truncate 72 }}
        template(v-else)
          .u-mg-t-12
            p.small There are no related reports.
            a.button.button--mini.button--hollow(
              v-link="{ name: 'file-a-report', query: { school: report.school }}"
            ) File a report

section.page__wrapper(:class="loading ? 'page--min-height' : ''")
  .content__wrapper
    .content__section
      template(v-if="!loading")
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
import { getReport } from '../../vuex/actions/report'

export default {
  vuex: {
    getters: {
      userID: ({ user }) => user.id,
      report: ({ report }) => report.view,
      loading: ({ report }) => report.buttonLoading
    },
    actions: {
      getReport,
      getID: ({ dispatch, state }) => {
        dispatch('REPORT_RECEIVE_ID', state.route.params.id)
      },
      updateUpvotes: ({ dispatch, state }, upvotes) => {
        dispatch('REPORT_UPDATE_UPVOTES', upvotes)
      },
      updateFollow: ({ dispatch, state }) => {
        dispatch('REPORT_UPDATE_FOLLOW')
      }
    }
  },
  computed: {
    hasAttachments () {
      if (typeof this.report.length !== 'undefined')
        return this.report.length > 0
      return false
    },
    detailText () {
      return this.report.text.split('\n\n')
    },
    googleMap () {
      return 'https://www.google.com/maps?q='
        + encodeURIComponent(this.report.school)
        + '&z=15&output=embed'
    }
  },
  data () {
    return {
      upvoting: false,
      following: false,
      relatedReports: []
    }
  },
  watch: {
    'report': function (val, oldVal) {
      if (typeof val.category !== 'undefined')
        this.getRelatedReports()
    },
    '$route.params.id': {
      handler: function() {
        this.getID()
        this.getReport(this)
      },
      immediate: true
    }
  },
  methods: {
    getRelatedReports () {
      this.$http.get(
        'report?school=' + this.report.school_id +
        '&exclude=' + this.report.id +
        '&limit=3'
      ).then(
        (response) => {
          this.relatedReports = response.data.reports
        },
        (response) => {
          console.log('Failed')
        }
      )
    },
    upvoteReport () {
      let data = {
            report_id: this.report.id,
            user_id: this.userID
          },
          endpoint = this.report.did_upvote ? 'unvote' : 'upvote'

      this.upvoting = true
      this.$http.post('report/' + endpoint, data).then(
        (response) => {
          this.updateUpvotes(response.data.upvotes)
          this.upvoting = false
        },
        (response) => {
          console.log('Failed to ' + endpoint)
        }
      )
    },
    followReport () {
      let data = {
            report_id: this.report.id,
            user_id: this.userID
          },
          endpoint = this.report.did_follow ? 'unfollow' : 'follow'

      this.following = true
      this.$http.post('report/' + endpoint, data).then(
        (response) => {
          this.updateFollow()
          this.following = false
        },
        (response) => {
          console.log('Failed to ' + endpoint)
        }
      )
    }
  },
  components: {
    'v-spinner': Spinner,
    'v-share-button': ShareButton
  }
}
</script>
