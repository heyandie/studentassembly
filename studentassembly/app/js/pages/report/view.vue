<template lang="jade">
section.page__wrapper.page--light
  .content__wrapper
    .content__section.u-mg-b-24
      article.content__main
        .spinner__wrapper(v-if="loading")
          v-spinner
          h4 Loading report...
        template(v-if="!loading")
          //- .form__wrapper
          .paragraph__section
            .button__group.pull-right
              a.button.button--tiny.button--light(href="#0") Follow
              .button.button--tiny.button--simple#share_menu(@click="openShareMenu = !openShareMenu")
                | •••
                .dropdown__menu(v-bind:class="openShareMenu ? 'dropdown__menu--open' : ''")
                  .dropdown__menu-header
                    span Share
                  a.dropdown__menu-item(target="_blank" href="#0")
                    img.button__icon(src="/static/img/fb-logo.png" height="15")
                    span Facebook
                  a.dropdown__menu-item(target="_blank" href="https://twitter.com/intent/tweet?text=Share%20Report")
                    img.button__icon(src="/static/img/twitter-logo.png" height="14")
                    span Twitter
            h2 {{ report.category }}
            h3.u-mg-b-24
              span.header--light {{ report.school }}
              small.list__item-remark.u-mg-t-8(:class="report.is_approved ? 'list__item--approved' : 'list__item--not-approved'")
                span {{ report.is_approved ? 'Approved' : 'Not Approved' }}
                span.list__item-date &nbsp;as of {{ report.updated_at | humanizeDate }}
            hr
          .paragraph__section(v-for="(index, question) in report.questions")
            h3 {{ question.text }}
            p {{ report.answers[index].text }}
          .paragraph__section
            h3 Details
            p {{ report.text }}
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
          hr.small
          template(v-for="related in relatedReports")
            .u-mg-t-24
              a(v-link="{ name: 'report-view', params: { id: related.id } }")
                h5 {{ related.category }}
                p.small {{ related.text | truncate }}

section.page__wrapper(:class="loading ? 'page--min-height' : ''")
  template(v-if="!loading")
    .content__full
      .content__half
        .content__section.content__half-left
          h4 {{ report.school }}
          small.light Manila, NCR
          hr.small
          p.small 400 reports
          p.small 224 resolved cases
          a.button.button--tiny.button--inverted(v-link="{ name: 'file-a-report', query: { school: report.school } }") File a report
          a.button.button--tiny.button--inverted(target="_blank" href="#0") Go to website
      .content__half
        .u-div-320
          .u-bg-img(:style="schoolLocation")

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
      let report = this.report.files
      return report && typeof report.length !== 'undefined'
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
        backgroundPosition: 'center',
        filter: 'grayscale(0)',
        backgroundImage: 'url("/static/img/map.jpg")'
      }

      if (typeof val.category !== 'undefined')
        this.getRelatedReports()
    },
    '$route.params.id': function() {
      this.getID()
      this.getReport(this)
    }
  },
  methods: {
    getRelatedReports () {
      this.$http.get('report?q=' + this.report.school.split(' ')[0] + '&limit=3').then(
        (response) => {
          this.relatedReports = response.data
        },
        (response) => {
          console.log('Failed')
        }
      )
    }
  },
  created () {
    this.getID()
    this.getReport(this)
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
