<template lang="jade">
section.page__wrapper
  .u-div-180(style="background-color:#293757;")
    .u-bg-img(style="opacity:0.1;background-image:url('/static/img/rating-header.jpg');")
section.page__wrapper.page--min-height
  .content__wrapper
    .content__section
      .u-pos-rel.u-mg-t-180-n
        h1.u-c-white.u-mg-b-4 Submit a Rating
        p.u-c-white.u-mg-b-24 Rate your professors, school administrators and staff
        .form__wrapper(v-if="!staff.length")
          .spinner__wrapper
            v-spinner
            h4 Loading staff members...
        template(v-else)
          .list__group
            .list__filters
              .list__search.list__search--full
                input(
                  type="text",
                  placeholder="Search by name or school",
                  :value="searchKey",
                  @input="updateSearchKey | debounce 250"
                )

            //- template(v-if="!filtered")
            //-   .list__empty(v-if="staff.length")
            //-     img.list__empty-icon(src="/static/img/icons/social/ic_sentiment_dissatisfied_48px.svg")
            //-     h3 No search results for '{{ searchKey }}'
            //-   .list__empty(v-else)
            //-     img.list__empty-icon(src="/static/img/icons/action/ic_assignment_48px.svg")
            //-     p.small No staff members available.
            //-
            //- template(v-if="(filtered) * (searchKey !== '')")
            //-   .list__results
            //-     h5 {{ filtered }} {{ filtered | pluralize 'result' }}

            table
              thead
                tr
                  th.u-cur-p(
                    v-for="param in params",
                    @click="updateSort(param)"
                  )
                    span {{ param | toTitleCase '_' }}
                    .sort-icon
                      img(
                        v-show="(sortKey === param) * (order === -1)",
                        src="/static/img/icons/hardware/ic_keyboard_arrow_down_24px.svg",
                        height="20"
                      )
                      img(
                        v-show="(sortKey === param) * (order === 1)",
                        src="/static/img/icons/hardware/ic_keyboard_arrow_up_24px.svg",
                        height="20"
                      )
              tbody
                tr.u-cur-p(
                  v-for="member in staff | orderBy sortKey order | filterBy searchKey in 'name' 'school'",
                  v-link="{ name: 'rate-view', params: { 'id': member.id }}"
                )
                  td(v-for="param in params") {{ member[param] }}
</template>

<script>
import Spinner from '../../components/spinner.vue'
import { getStaff } from '../../vuex/actions/staff'

export default {
  vuex: {
    getters: {
      staff: ({ staff }) => staff.all,
      params: ({ staff }) => staff.params,
      searchKey: ({ staff }) => staff.searchKey,
      sortKey: ({ staff }) => staff.sortKey,
      order: ({ staff }) => staff.order
    },
    actions: {
      getStaff,
      updateSearchKey: ({ dispatch }, e, init = false) => {
        dispatch('STAFF_UPDATE_SEARCHKEY', init ? e : e.target.value)
      },
      updateSort: ({ dispatch }, sortKey) => {
        dispatch('STAFF_UPDATE_SORT', sortKey)
      }
    }
  },
  route: {
    data ({ to: { query: { school }}}) {
      this.updateSearchKey(school, true)
    }
  },
  created () {
    this.getStaff(this)
  },
  components: {
    'v-spinner': Spinner
  }
}
</script>
