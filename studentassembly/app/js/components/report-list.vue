<template lang="jade">
.list__group
  .spinner__wrapper(v-if="loading")
    v-spinner
    h4 Loading reports...
  template(v-if="!loading")
    template(v-if="hasReports")
      .list__filters(v-if="filters")
        .list__search.pull-left
          input(type="text", placeholder="Search by school or category", v-model="searchKey", @input="resetPagination")
        .list__options.pull-right
          .form__select
            select(name="sort-by")
              option(disabled selected hidden value="") Filter by status
              option(value="for-verification") For Verification
              option(value="under-investigation") Under Investigation
              option(value="resolved") Resolved
              option(value="unresolved") Unresolved
    template(v-if="!filteredLength")
      .list__empty(v-if="hasReports")
        img.list__empty-icon(src="/static/img/icons/social/ic_sentiment_dissatisfied_48px.svg")
        h3 No search results for '{{ searchKey }}'
      .list__empty(v-if="!hasReports")
        img.list__empty-icon(src="/static/img/icons/action/ic_assignment_48px.svg")
        h3 You don't have reports yet.
        p.small Start by filing a corruption report. You can also look for existing reports by using the search bar on the topmost area of the page.
        a.button.button--small(v-link="{ name: 'file-a-report' }") File a report
    template(v-if="filteredAndHasSearchkey")
      .list__results
        h5 {{ filteredLength }} {{ filteredLength | pluralize 'result' }}
    a.list__item(
      v-for="report in reports | filterBy searchKey in 'category' 'school' | count | limitBy limit offset",
      v-link="{ name: 'report-view', params: { id: report.id } }"
    )
      h4
        .pull-right
          small.list__item-remark(:class="report.is_approved ? 'list__item--approved' : 'list__item--not-approved'")
            | {{ report.is_approved ? 'Resolved' : 'Unresolved' }}
        span {{ report.category }}
        br
        small {{ report.school }}
      p.small {{ report.updated_at | relativeDate | capitalize }}
      p {{ report.text | truncate }}

    .list__pagination(v-if="moreThanLimit")
      .list__page(
        v-for="i in reports.length / limit",
        :class="i === currentPage ? 'list__page--current' : ''",
        @click="goToPage(i)"
      )
        | {{ i + 1 }}
</template>

<script>
import RelativeDate from 'relative-date'
import Spinner from './spinner.vue'

export default {
  props: ['loading', 'reports', 'filters'],
  data () {
    return {
      limit: 10,
      lastPage: 0,
      currentPage: 0,
      searchKey: '',
      filteredLength: null
    }
  },
  methods: {
    resetPagination (e) {
      if (e.target.value.length === 1)
        this.lastPage = this.currentPage
      this.currentPage = e.target.value.length > 0 ? 0 : this.lastPage
    },
    goToPage (page) {
      this.currentPage = page
      window.scrollTo(0, 0)
    }
  },
  computed: {
    offset () {
      return this.limit * this.currentPage
    },
    hasReports () {
      return this.reports.length > 0
    },
    filteredAndHasSearchkey () {
      return this.filteredLength && this.searchKey !== ''
    },
    moreThanLimit () {
      return this.reports.length > this.limit && this.searchKey === ''
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
    'v-spinner': Spinner
  }
}
</script>
