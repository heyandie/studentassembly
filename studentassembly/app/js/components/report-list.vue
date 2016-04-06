<template lang="jade">
.list__group
  .spinner__wrapper(v-if="loading")
    v-spinner
  template(v-if="!loading")
    .list__filters(v-if="filters")
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
    template(v-if="filteredAndNonEmpty")
      .list__results
        h5 {{ filteredLength }} {{ filteredLength | pluralize 'result' }}
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
      p.small {{ report.updated_at | relativeDate | capitalize }}
      p {{ report.text | truncate }}
</template>

<script>
import RelativeDate from 'relative-date'
import Spinner from './spinner.vue'

export default {
  props: ['loading', 'reports', 'filters'],
  data () {
    return {
      searchKey: '',
      filteredLength: null
    }
  },
  computed: {
    filteredAndNonEmpty () {
      return this.filteredLength && this.searchKey !== ''
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
