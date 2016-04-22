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
        a.button.button--block.button--small.button--inverted(href="#0") Edit profile


      article.content__main
        .tabs
          .tabs__nav
            .tab__nav(v-on:click="activeTab = 'reports'" v-bind:class="activeTab === 'reports' ? 'active' : ''")
              h4
                | Reports&nbsp;
                span.header--light {{ reportCount }}
            .tab__nav(v-on:click="activeTab = 'ratings'" v-bind:class="activeTab === 'ratings' ? 'active' : ''")
              h4
                | Ratings&nbsp;
                span.header--light 3
            .tab__nav(v-on:click="activeTab = 'following'" v-bind:class="activeTab === 'following' ? 'active' : ''")
              h4
                | Following&nbsp;
                span.header--light 10
          .tabs__content
            .tab__content(v-if="activeTab === 'reports'")
              v-report-list(v-bind:reports="reports" v-bind:loading="loading" v-bind:filters="true")
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
