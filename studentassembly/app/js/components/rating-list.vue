<template lang="jade">
.list
  .spinner__wrapper(v-if="loading")
    v-spinner
    h4 Loading ratings...

  .list__group(v-else)
    template(v-if="ratings.length")
      .list__filters(v-if="filters")
        .list__search.list__search--full
          input(
            type="text",
            placeholder="Search by name or school",
            v-model="searchKey",
            @input="resetPagination | debounce 250"
          )
    .list__empty(v-else)
      slot(name="list_empty")

    .list__empty(v-if="(!filteredCount) * (ratings.length)")
      img.list__empty-icon(src="/static/img/icons/social/ic_sentiment_dissatisfied_48px.svg")
      h3 No search results for '{{ searchKey }}'

    .list__results(v-if="(filteredCount) * (searchKey !== '')")
      h5 {{ filteredCount }} {{ filteredCount | pluralize 'result' }}

    a.list__item(
      v-for="rating in ratings | filterBy searchKey in 'staff_name' 'school' | count | limitBy limit offset",
      v-link="{ name: 'rate-view', params: { id: rating.staff_id } }"
    )
      h4
        span {{ rating.staff_name }}
        br
        small {{ rating.school }}
      ul.stats.u-mg-t-16
        li.stat.stat--small(v-for="val in rating.values | orderObjectKeys")
          p.stat__header {{ $key | toTitleCase '_' }}
          span.stat__value {{ val }} / 5

    .list__pagination(v-if="moreThanLimit")
      .list__page(
        v-for="i in ratings.length / limit",
        :class="i === currentPage ? 'list__page--current' : ''",
        @click="setPage(i)"
      ) {{ i + 1 }}
</template>

<script>
import Spinner from './spinner.vue'

export default {
  props: ['loading', 'ratings', 'filters'],
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
      return this.ratings.length > this.limit && this.searchKey === ''
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
