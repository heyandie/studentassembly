<template lang="jade">
v-header
section.page__wrapper
  .content__wrapper
    .content__section
      aside.content__secondary
        h3.u-ta-c Hello, {{ username }}!
        //- a.button.button--small.button--inverted(href="#0") Edit profile
        hr
        //- h4
        //-   img(src="/static/img/icons/editor/ic_show_chart_24px.svg" height="18")
        //-   span Quick stats
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
              .list__group
                .spinner__wrapper(v-if="loading")
                  v-spinner
                template(v-if="!loading")
                  .list__filters
                    .list__search.pull-left
                      input(type="text" placeholder="Search by school or category" v-model="searchKey")
                    .list__options.pull-right
                      .form__select
                        select(name="sort-by")
                          option(disabled selected hidden value="") Filter by status
                          option(value="for-verification") For Verification
                          option(value="under-investigation") Under Investigation
                          option(value="resolved") Resolved
                          option(value="unresolved") Unresolved
                  template(v-if="!filteredLength")
                    .list__empty
                      img.list__empty-icon(src="/static/img/icons/social/ic_sentiment_dissatisfied_48px.svg")
                      h3 No search results for '{{ searchKey }}'
                  //- template(v-if="filteredLength")
                  //-   .list__results
                  //-     h5 {{ filteredLength }} results
                  a.list__item(
                    v-for="report in reports | filterBy searchKey in 'category' 'school' | count"
                    v-link="{ name: 'report-view', params: { id: report.id } }"
                  )
                    h4
                      .pull-right
                        small.list__item-remark(:class="report.is_approved ? 'list__item--approved' : 'list__item--not-approved'")
                          | {{ report.is_approved ? 'Resolved' : 'Unresolved' }}
                      span {{ report.category }}
                      br
                      small {{ report.school }}
                    p.small {{ report.updated_at | relativeDate }}
                    p {{ report.text | truncate }}
</template>

<script>
import RelativeDate from 'relative-date'

import Header from '../../components/header.vue'
import Footer from '../../components/footer.vue'
import Spinner from '../../components/spinner.vue'

import { getProfile, getReports } from '../../vuex/actions/user'

export default {
  vuex: {
    getters: {
      username: ({ user }) => user.username,
      reports: ({ user }) => user.reports,
      reportCount: ({ user }) => user.report_count,
      loading: ({ report }) => report.buttonLoading
    },
    actions: {
      getProfile,
      getReports
    }
  },
  data () {
    return {
      activeTab: 'reports',
      searchKey: '',
      filteredLength: null
    }
  },
  created () {
    this.getProfile()
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
  filters: {
    truncate (string) {
      if (string.length > 140)
        return string.substring(0, 140) + '...'
      else
        return string
    },
    count (arr) {
      this.$set('filteredLength', arr.length)
      return arr
    },
    relativeDate (date) {
      return RelativeDate(Date.parse(date))
    }
  },
  components: {
    'v-header': Header,
    'v-footer': Footer,
    'v-spinner': Spinner
  }
}
</script>
