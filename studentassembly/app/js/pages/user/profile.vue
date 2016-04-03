<template lang="jade">
v-header
section.page__wrapper
  .content__wrapper
    .content__section
      aside.content__secondary
        h2 Hello, {{ username }}!
        p.small
          a(href="#0") Edit profile
        hr
        h4
          img(src="/static/img/icons/editor/ic_show_chart_24px.svg" height="18")
          span Stats
        ul
          li
            p.small Resolved cases: n
          li
            p.small Dismissed cases: n

      article.content__main
        h3 Your Reports ({{ reports.length }})
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
      loading: ({ report }) => report.buttonLoading
    },
    actions: {
      getProfile,
      getReports
    }
  },
  data () {
    return {
      searchKey: '',
      filteredLength: null
    }
  },
  created () {
    this.getProfile()
    this.getReports(this)
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
