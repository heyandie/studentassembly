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
              .button.button--tiny.button--simple#share_menu(@click="openShareMenu = !openShareMenu")
                span.u-c-facebook •
                span.u-c-twitter •
                span.u-c-brand •
                .dropdown__menu(v-bind:class="openShareMenu ? 'dropdown__menu--open' : ''")
                  .dropdown__menu-header
                    span Share
                  a.dropdown__menu-item(
                    @click.prevent="shareDialog('https://facebook.com/sharer/sharer.php?u=http%3A%2F%2Fstudentassembly.herokuapp.com%2F')"
                  )
                    img.button__icon(src="/static/img/fb-logo.png", height="15")
                    span Facebook
                  a.dropdown__menu-item(
                    @click.prevent="shareDialog('https://twitter.com/intent/tweet?text=Share%20Report')"
                  )
                    img.button__icon(src="/static/img/twitter-logo.png", height="14")
                    span Twitter
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
    shareDialog (url, width = 570, height = 370) {
      let left = (screen.width / 2) - (width / 2),
          top = (screen.height / 2) - (height / 2) - 80
      window.open(url, '',
        'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,width=' +
        width + ',height=' + height + ',top=' + top + ',left=' + left
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
