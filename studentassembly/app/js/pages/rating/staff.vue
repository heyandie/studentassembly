<template lang="jade">
section.page__wrapper
  .u-div-180(style="background-color:#293757;")
    .u-bg-img(style="opacity:0.1;background-image:url('/static/img/report-header.jpg');")
section.page__wrapper.page--min-height
  .content__wrapper
    .content__section
      .u-pos-rel.u-mg-t-180-n
        h1.u-c-white.u-mg-b-4 Submit a Rating
        p.u-c-white.u-mg-b-24 Rate your professors, school administrators and staff
        .form__wrapper(v-if="$loadingRouteData")
          .spinner__wrapper
            v-spinner
            h4 Loading staff members...
        template(v-if="!$loadingRouteData")
          .list__group
            .list__filters
              .list__search.list__search--full
                input(type="text", placeholder="Search by name or school", v-model="searchKey")
            table
              thead
                tr
                  th.u-cur-p(
                    v-for="param in params",
                    v-on:click="sortBy(param)"
                  )
                    span {{ toTitleCase(param, '_') }}
                    .sort-icon
                      img(v-show="isDescending(param)", src="/static/img/icons/hardware/ic_keyboard_arrow_down_24px.svg", height="20")
                      img(v-show="isAscending(param)", src="/static/img/icons/hardware/ic_keyboard_arrow_up_24px.svg", height="20")
              tbody
                tr.u-cur-p(
                  v-for="member in staff | orderBy sortKey order | filterBy searchKey in 'name' 'school'",
                  v-link="{ name: 'rate-view', params: { 'id': member.id } }"
                  )
                  td(v-for="param in params") {{ member[param] }}
</template>

<script>
import Spinner from '../../components/spinner.vue'
import { toTitleCase } from '../../util'

export default {
  route: {
    data (transition) {
      return this.$http.get('staff').then(
        (response) => {
          let staff = response.data
          staff.forEach((mem) => {
            Object.defineProperty(mem, 'rating_-_overall', {
              get () { return this.rating.overall }
            })
          })
          this.staff = staff
        },
        (response) => {
          console.log('Failed to retrieve staff list.')
        }
      )
    }
  },
  data () {
    return {
      params: ['name', 'school', 'rating_-_overall'],
      searchKey: this.$route.query.school || '',
      sortKey: 'rating_-_overall', // TODO: discuss implications
      order: -1,
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
      return this.sortKey === sortKey && this.order === 1
    },
    isDescending (sortKey) {
      return this.sortKey === sortKey && this.order === -1
    }
  },
  components: {
    'v-spinner': Spinner
  }
}
</script>
