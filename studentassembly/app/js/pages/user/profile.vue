<template lang="jade">
section.page__wrapper.page--min-height
  .content__wrapper
    .content__section
      .u-cf
        .u-fl-l
          h3
            v-avatar(:alias="alias", :inline="true", height="36px", width="36px")
            span Hello, {{ alias }}!
        .u-fl-r
          a.button.button--tiny.button--inverted(href="#0", @click.prevent="editProfile") Edit profile
      hr
      .tabs
        .tabs__nav
          .tab__nav(@click="activeTab = 'reports'", :class="activeTab === 'reports' ? 'active' : ''")
            p.small
              strong Reports
              small.light &nbsp;&nbsp;{{ reports.length }}
          .tab__nav(@click="activeTab = 'ratings'", :class="activeTab === 'ratings' ? 'active' : ''")
            p.small
              strong Ratings
              small.light &nbsp;&nbsp;{{ ratings.length }}
          .tab__nav(@click="activeTab = 'upvoted'", :class="activeTab === 'upvoted' ? 'active' : ''")
            p.small
              strong Upvoted
              small.light &nbsp;&nbsp;{{ upvoted.length }}
          .tab__nav(@click="activeTab = 'following'", :class="activeTab === 'following' ? 'active' : ''")
            p.small
              strong Following
              small.light &nbsp;&nbsp;{{ following.length }}

      article.content__main
        .tabs
          .tabs__content
            .tab__content(v-show="activeTab === 'reports'")
              v-report-list(:reports="reports", :loading="loading", :filters="true")
                template(slot="list_empty")
                  img.list__empty-icon(src="/static/img/icons/action/ic_assignment_48px.svg")
                  h3 You don't have reports yet.
                  p.small Start by filing a corruption report. You can also look for existing reports by using the search bar on the topmost area of the page.
                  a.button.button--small(v-link="{ name: 'file-a-report' }") File a report
            .tab__content(v-show="activeTab === 'ratings'")
              v-rating-list(:ratings="ratings", :loading="loading", :filters="true")
                template(slot="list_empty")
                  img.list__empty-icon(src="/static/img/icons/action/ic_assignment_ind_48px.svg")
                  h3 You have not rated anyone yet.
                  p.small Start by looking for staff members in your school. You can also look for existing ratings by using the search bar on the topmost area of the page.
                  a.button.button--small(v-link="{ name: 'rate-staff' }") Submit a rating
            .tab__content(v-show="activeTab === 'upvoted'")
              v-report-list(:reports="upvoted", :loading="loading", :filters="true", :show-alias="true")
                template(slot="list_empty")
                  img.list__empty-icon(src="/static/img/icons/action/ic_assignment_late_48px.svg")
                  h3 No upvotes to see here.
                  p.small Make other reports visible by upvoting them! Your reports are automatically upvoted, so you won't see them here.
            .tab__content(v-show="activeTab === 'following'")
              v-report-list(:reports="following", :loading="loading", :filters="true", :show-alias="true")
                template(slot="list_empty")
                  img.list__empty-icon(src="/static/img/icons/action/ic_assignment_turned_in_48px.svg")
                  h3 You have not followed any report.
                  p.small Follow reports so you can receive updates regarding their statuses. Your reports are automatically followed, so you won't see them here.

      aside.content__secondary.content--additional-info
        template(v-if="reports")
          h4 Profile stats
          .u-mg-t-12
            p.small
              | (reports by category, ratings, etc)

  v-modal(:show.sync="showEditProfileModal")
    div(slot="content", style="width:320px;")
      i.modal-close.icon.ion-android-close(@click="showEditProfileModal = false")
      .spinner__wrapper(v-if="profileInfo === null")
        v-spinner
      form(v-else)
        .form__element
          .form__label Email address
          input(type="email", v-model="profileInfo.email", placeholder="juan@student.ph")
        .form__element
          .form__label Name
          .form__note Fill this if you want to pursue legal action when reporting.
          input(type="text", v-model="profileInfo.name", placeholder="Juan dela Cruz")
        .form__element
          .form__label Mobile number
          .form__note Fill this if you want to pursue legal action when reporting.
          input(type="text", v-model="profileInfo.contact_number", placeholder="+63 9xx xxx xxxx")
        .form__element
          button(type="submit", @click.prevent="submitProfile") Submit
</template>

<script>
import Modal from '../../components/modal.vue'
import ReportList from '../../components/report-list.vue'
import RatingList from '../../components/rating-list.vue'
import Avatar from '../../components/avatar.vue'
import Spinner from '../../components/spinner.vue'
import { getReports, getRatings } from '../../vuex/actions/user'

export default {
  vuex: {
    getters: {
      userID: ({ user }) => user.id,
      alias: ({ user }) => user.alias,
      reports: ({ user }) => user.reports,
      ratings: ({ user }) => user.ratings,
      upvoted: ({ user }) => user.upvoted,
      following: ({ user }) => user.following,
      loading: ({ report }) => report.buttonLoading
    },
    actions: {
      getReports, getRatings
    }
  },
  data () {
    return {
      activeTab: 'reports',
      showEditProfileModal: false,
      profileInfo: null
    }
  },
  created () {
    this.getReports(this)
    this.getRatings(this)
  },
  methods: {
    editProfile () {
      this.showEditProfileModal = !this.showEditProfileModal
      if (this.showEditProfileModal && this.profileInfo === null) {
        this.$http.get('user', { contact: 'true' }).then(
          (response) => {
            this.profileInfo = response.data
          },
          (response) => {
            console.log('Failed to get user info.')
          }
        )
      }
    },
    submitProfile () {
      this.$http.patch('account/' + this.userID, this.profileInfo).then(
        (response) => {
          this.showEditProfileModal = false
        },
        (response) => {
          console.log('Failed to patch user info.')
        }
      )
    }
  },
  components: {
    'v-modal': Modal,
    'v-report-list': ReportList,
    'v-rating-list': RatingList,
    'v-avatar': Avatar,
    'v-spinner': Spinner
  }
}
</script>
