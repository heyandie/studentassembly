<template lang="jade">
v-header
section.page__wrapper
  .content__wrapper
    .content__section
      h1 Rate staff
      .form__wrapper(v-if="loading")
        .spinner__wrapper
          v-spinner
        h4.u-ta-c Loading list of staff members...
      template(v-if="!loading")
        table
          thead
            tr
              th.u-cur-p(
                v-for="param in params"
                v-on:click="sortBy(param)"
              )
                span {{ toTitleCase(param, '_') }}
                .sort-icon
                  img(v-show="isDescending(param)" src="/static/img/icons/hardware/ic_keyboard_arrow_down_24px.svg" height="20")
                  img(v-show="isAscending(param)" src="/static/img/icons/hardware/ic_keyboard_arrow_up_24px.svg" height="20")
          tbody
            tr.u-cur-p(
              v-for="member in staff | orderBy sortKey order"
              v-link="{ name: 'rate-view', params: { 'id': member.id } }"
              )
              td(v-for="param in params") {{ member[param] }}
</template>

<script>
import Header from '../../components/header.vue'
import Spinner from '../../components/spinner.vue'
import { toTitleCase } from '../../util'

export default {
  data () {
    return {
      loading: true,
      params: ['name', 'school', 'overall_rating'],
      sortKey: 'overall_rating', // TODO: discuss implications
      order: 1,
      staff: []
    }
  },
  methods: {
    toTitleCase: toTitleCase,
    sortBy (sortKey) {
      this.order = (this.sortKey === sortKey) ? this.order * -1 : 1
      this.sortKey = sortKey
    },
    isAscending (sortKey) {
      return this.sortKey === sortKey && this.order === -1
    },
    isDescending (sortKey) {
      return this.sortKey === sortKey && this.order === 1
    }
  },
  created () {
    this.$http.get('staff').then(
      function(response) {
        this.staff = response.data
        this.loading = false
      },
      function(response) {
        console.log('Failed to retrieve staff list.')
      }
    )
  },
  components: {
    'v-header': Header,
    'v-spinner': Spinner
  }
}
</script>
