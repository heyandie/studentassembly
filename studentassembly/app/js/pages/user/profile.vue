<template lang="jade">
section.page__wrapper.page--min-height
  .content__wrapper
    .content__section
      .u-cf
        .pull-left
          h3
            v-avatar(:alias="alias", :inline="true", height="36px", width="36px")
            span Hello, {{ alias }}!
        .pull-right
          a.button.button--tiny.button--inverted(href="#0", @click.prevent="showEditProfileModal = true") Edit profile
      hr
      .tabs
        .tabs__nav
          .tab__nav(@click="activeTab = 'reports'", :class="activeTab === 'reports' ? 'active' : ''")
            p.small
              strong Reports
              small.light &nbsp;&nbsp;{{ reportCount }}
          .tab__nav(@click="activeTab = 'ratings'", :class="activeTab === 'ratings' ? 'active' : ''")
            p.small
              strong Ratings
              small.light &nbsp;&nbsp;3
          .tab__nav(@click="activeTab = 'upvoted'", :class="activeTab === 'upvoted' ? 'active' : ''")
            p.small
              strong Upvoted
              small.light &nbsp;&nbsp;6
          .tab__nav(@click="activeTab = 'following'", :class="activeTab === 'following' ? 'active' : ''")
            p.small
              strong Following
              small.light &nbsp;&nbsp;10
      article.content__main
        .tabs
          .tabs__content
            .tab__content(v-if="activeTab === 'reports'")
              v-report-list(:reports="reports", :loading="loading", :filters="true", :on-profile="true")
      aside.content__secondary.content--additional-info
        template(v-if="reports")
          h4 Profile stats
          .u-mg-t-12
            p.small
              | (reports by category, ratings, etc)
          //- template(v-else)
          //-   .u-mg-t-24(v-for="upvoted in reports | limitBy 3")
          //-     a(v-link="{ name: 'report-view', params: { id: upvoted.id } }")
          //-       h5 {{ upvoted.category }}
          //-       p.small {{ upvoted.text | truncate }}
          //-   .u-mg-t-24
          //-     a.button.button--tiny.button--light(href="#0") Load more

v-modal(:show.sync="showEditProfileModal")
  div(slot="content", style="width:320px;")
    i.modal-close.icon.ion-android-close(@click="showEditProfileModal = false")
    //- h3 Edit your profile
    .spinner__wrapper
      v-spinner
    form
      .form__element
        .form__label Email address
        input(type="email" placeholder="Your current email")
      .form__element
        .form__label Name
        input(type="text" placeholder="Name")
      .form__element
        .form__label Mobile number
        input(type="text" placeholder="Mobile")
      .form__element
        button(type="submit", @click.prevent="true") Submit
</template>

<script>
import Modal from '../../components/modal.vue'
import ReportList from '../../components/report-list.vue'
import Avatar from '../../components/avatar.vue'
import Spinner from '../../components/spinner.vue'
import { getReports } from '../../vuex/actions/user'

export default {
  vuex: {
    getters: {
      alias: ({ user }) => user.alias,
      reports: ({ user }) => user.reports,
      reportCount: ({ user }) => user.report_count,
      loading: ({ report }) => report.buttonLoading
    },
    actions: {
      getReports
    }
  },
  data () {
    return {
      activeTab: 'reports',
      showEditProfileModal: false
    }
  },
  created () {
    this.getReports(this)
  },
  // watch: {
  //   'reports': function () {
  //     console.log(JSON.stringify(this.reports).length)
  //   }
  // },
  filters: {
    truncate (string) {
      if (string.length > 72)
        return string.substring(0, 72) + '...'
      else
        return string
    }
  },
  computed: {
    resolvedReportsCount () {
      return this.$options.filters.filterBy(this.reports, 'true', 'is_approved').length
    },
    unresolvedReportsCount () {
      return this.$options.filters.filterBy(this.reports, 'false', 'is_approved').length
    }
  },
  components: {
    'v-modal': Modal,
    'v-report-list': ReportList,
    'v-avatar': Avatar,
    'v-spinner': Spinner
  }
}
</script>
