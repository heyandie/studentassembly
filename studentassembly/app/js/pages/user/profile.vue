<template lang="jade">
section.page__wrapper.page--min-height
  .content__wrapper
    .content__section
      aside.content__secondary
        v-avatar(v-bind:alias="alias")
        h3.u-ta-c Hello, {{ alias }}!
        hr
        ul.stats
          li.stat
            p.stat__header Resolved
            span.stat__value {{ resolvedReportsCount }}
          li.stat
            p.stat__header Unresolved
            span.stat__value {{ unresolvedReportsCount }}
          li.stat
            p.stat__header Upvoted
            span.stat__value 3
        hr
        .button__group.u-ta-c
          a.button.button--tiny.button--light(href="#0") Edit profile
      article.content__main
        .tabs
          .tabs__nav
            .tab__nav(@click="activeTab = 'reports'", :class="activeTab === 'reports' ? 'active' : ''")
              h4
                | Reports&nbsp;
                span.header--light {{ reportCount }}
            .tab__nav(@click="activeTab = 'ratings'", :class="activeTab === 'ratings' ? 'active' : ''")
              h4
                | Ratings&nbsp;
                span.header--light 3
            .tab__nav(@click="activeTab = 'following'", :class="activeTab === 'following' ? 'active' : ''")
              h4
                | Following&nbsp;
                span.header--light 10
          .tabs__content
            .tab__content(v-if="activeTab === 'reports'")
              v-report-list(:reports="reports", :loading="loading", :filters="true")
</template>

<script>
import ReportList from '../../components/report-list.vue'
import Avatar from '../../components/avatar.vue'
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
      activeTab: 'reports'
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
  computed: {
    resolvedReportsCount () {
      return this.$options.filters.filterBy(this.reports, 'true', 'is_approved').length
    },
    unresolvedReportsCount () {
      return this.$options.filters.filterBy(this.reports, 'false', 'is_approved').length
    }
  },
  components: {
    'v-report-list': ReportList,
    'v-avatar': Avatar
  }
}
</script>
