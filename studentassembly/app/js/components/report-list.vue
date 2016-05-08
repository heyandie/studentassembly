<template lang="jade">
.list
  .spinner__wrapper(v-if="loading" transition="fade")
    v-spinner
    h4 Loading reports...

  .list__group(v-else transition="fade")
    template(v-if="reports.length")
      .list__filters(v-if="filters")
        .list__search.u-fl-l
          input(
            type="text",
            placeholder="Search by category or school",
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

    template(v-if="!filteredCount")
      .list__empty(v-if="reports.length")
        img.list__empty-icon(src="/static/img/icons/social/ic_sentiment_dissatisfied_48px.svg")
        h3 No search results for '{{ searchKey }}'
      .list__empty(v-else)
        slot(name="list_empty")

    template(v-if="(filteredCount) * (searchKey !== '')")
      .list__results
        h5 {{ filteredCount }} {{ filteredCount | pluralize 'result' }}

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
        @click="setPage(i)"
      ) {{ i + 1 }}
</template>

<script>
import Spinner from './spinner.vue'

export default {
  props: ['loading', 'reports', 'filters'],
  data () {
    return {
      limit: 10,
      lastPage: 0,
      currentPage: 0,
      searchKey: '',
      filteredCount: 0
    }
  },
  methods: {
    resetPagination (e) {
      if (e.target.value.length === 1)
        this.lastPage = this.currentPage
      this.currentPage = e.target.value.length > 0 ? 0 : this.lastPage
    },
    setPage (page) {
      this.currentPage = page
      window.scrollTo(0, 0)
    }
  },
  computed: {
    offset () {
      return this.limit * this.currentPage
    },
    moreThanLimit () {
      return this.reports.length > this.limit && this.searchKey === ''
    }
  },
  filters: {
    count (arr) {
      this.$set('filteredCount', arr.length)
      return arr
    }
  },
  components: {
    'v-spinner': Spinner
  }
}
</script>
