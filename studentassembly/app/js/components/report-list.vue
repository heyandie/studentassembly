<template lang="jade">
.list__group
  .spinner__wrapper(v-if="loading")
    v-spinner
    h4 Loading reports...

  template(v-if="!loading")
    template(v-if="hasReports")
      .list__filters(v-if="filters")
        .list__search.u-fl-l
          input(
            type="text",
            placeholder="Search by school or category",
            v-model="searchKey",
            @input="resetPagination | debounce 250"
          )
        .list__options.u-fl-r
          .form__select
            select(name="sort-by")
              option(disabled selected hidden value="") Status
              option(value="pending") Pending
              option(value="accepted") Accepted
              option(value="resolved") Resolved

    template(v-if="!filtered")
      .list__empty(v-if="hasReports")
        img.list__empty-icon(src="/static/img/icons/social/ic_sentiment_dissatisfied_48px.svg")
        h3 No search results for '{{ searchKey }}'
      .list__empty(v-if="!hasReports")
        slot(name="list_empty")

    template(v-if="filteredAndHasSearchkey")
      .list__results
        h5 {{ filtered }} {{ filtered | pluralize 'result' }}

    a.list__item(
      v-for="report in reports | filterBy searchKey in 'category' 'school' | count | limitBy limit offset",
      v-link="{ name: 'report-view', params: { id: report.id } }"
    )
      h4
        .u-fl-r
          small.list__item-remark(:class="report.is_approved ? 'list__item--approved' : 'list__item--not-approved'")
            | {{ report.status }}
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
      ) {{ i + 1 }}
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
      filtered: 0
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
      return this.filtered && this.searchKey !== ''
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
      this.$set('filtered', arr.length)
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
