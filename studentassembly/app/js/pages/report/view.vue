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
              a.button.button--tiny.button--light(href="#0", @click.prevent="testUpvote")
                span {{ report.vote ? 'Upvoted' : 'Upvote' }}
              a.button.button--tiny.button--simple(href="#0") Follow
              .button.button--tiny.button--simple#share_menu(@click="openShareMenu = !openShareMenu")
                span.u-c-facebook •
                span.u-c-twitter •
                span.u-c-brand •
                .dropdown__menu(v-bind:class="openShareMenu ? 'dropdown__menu--open' : ''")
                  .dropdown__menu-header
                    span Share
                  a.dropdown__menu-item(target="_blank", href="#0")
                    img.button__icon(src="/static/img/fb-logo.png", height="15")
                    span Facebook
                  a.dropdown__menu-item(target="_blank", href="https://twitter.com/intent/tweet?text=Share%20Report")
                    img.button__icon(src="/static/img/twitter-logo.png", height="14")
                    span Twitter
            h2 {{ report.category }}
            h3.u-mg-b-24
              span.header--light {{ report.school }}
              small.list__item-remark.u-mg-t-8(
                :class="report.is_approved ? 'list__item--approved' : 'list__item--not-approved'"
              )
                span {{ report.status }}
                span.list__item-date &nbsp;as of {{ report.updated_at | humanizeDate }}, reported by {{ report.alias }}
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
        template(v-if="relatedReports.length")
          h4 Other reports in this school
          .u-mg-t-24(v-for="related in relatedReports")
            a(v-link="{ name: 'report-view', params: { id: related.id }}")
              h5 {{ related.category }}
              p.small {{ related.text | truncate }}

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
          .u-div-240
            .u-bg-img(:style="schoolLocation")

</template>

<script>
import Spinner from '../../components/spinner.vue'
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
      }
    }
  },
  filters: {
    humanizeDate (date) {
      return new Date(date).toDateString()
    },
    truncate (string) {
      if (string.length > 72)
        return string.substring(0, 72) + '...'
      else
        return string
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
    }
  },
  data () {
    return {
      openShareMenu: false,
      relatedReports: [],
      schoolLocation: {}
    }
  },
  watch: {
    'report': function (val, oldVal) {
      this.schoolLocation = {
        backgroundImage: 'url("/static/img/map.jpg")',
        backgroundPosition: 'center',
        backgroundSize: 'auto',
        filter: 'grayscale(0)'
      }

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
      this.$http.get('report?school=' + this.report.school_id + '&limit=3').then(
        (response) => {
          this.relatedReports = response.data.reports
        },
        (response) => {
          console.log('Failed')
        }
      )
    },
    testUpvote () {
      let data = {
        report_id: this.report.id,
        user_id: this.userID
      }
      // this.$http.post('report/upvote', data).then(
      //   (response) => {
      //     console.log(response)
      //   },
      //   (response) => {
      //     console.log('Failed')
      //   }
      // )
    }
  },
  ready () {
    document.addEventListener("keydown", (e) => {
      if (this.openShareMenu && e.keyCode == 27)
        this.openShareMenu = false
    })
    document.addEventListener("click", (e) => {
      if (e.target.id !== 'share_menu')
        this.openShareMenu = false
    })
  },
  components: {
    'v-spinner': Spinner
  }
}
</script>
