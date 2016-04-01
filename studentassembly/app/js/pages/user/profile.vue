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
          .list__filters
            .list__search.pull-left
              input(type="text" placeholder="Search by school or category" v-model="searchKey")
            //- .list__options.pull-right
            //-   .form__select
            //-     select(name="sort-by")
            //-       option(disabled selected hidden value="0") Filter by status
            //-       option Waiting for approval
          .spinner__wrapper(v-if="loading")
            v-spinner
          template(v-if="!loading")
            a.list__item(v-for="report in reports | filterBy searchKey in 'category' 'school'" v-link="{ name: 'report-view', params: { id: report.id } }")
              h4
                .pull-right
                  small.list__item-remark(:class="report.is_approved ? 'list__item--approved' : 'list__item--not-approved'") {{ report.is_approved ? 'Approved' : 'Not Approved' }}
                span {{ report.category }}
                br
                small {{ report.school }}
              p.small.list__date {{ report.updated_at }}
              p {{ report.text | truncate }}
</template>

<script>
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
      searchKey: ''
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
    }
  },
  components: {
    'v-header': Header,
    'v-footer': Footer,
    'v-spinner': Spinner
  }
}
</script>
