<template lang="jade">
section.page__wrapper
  .content__wrapper
    .content__section
      //- article.content__main
      .list__group
        a.list__item(
          v-for="member in staff"
          v-link="{ name: 'rate-view', params: { 'id': member.id } }"
        )
          h4
            span {{ member.name }}
            br
            small {{ member.school }}
          ul
            li(v-for="(key, val) in member.rating")
              strong {{ toTitleCase(key, '_') }}
              span &nbsp;{{ val }}
</template>

<script>
import Avatar from '../../components/avatar.vue'
import { toTitleCase } from '../../util'

export default {
  data () {
    return {
      staff: []
    }
  },
  methods: {
    toTitleCase: toTitleCase
  },
  created () {
    this.$http.get('staff').then(
      function(response) {
        this.staff = response.data
      },
      function(response) {
        console.log('Failed to retrieve staff list.')
      }
    )
  },
  components: {
    'v-avatar': Avatar
  }
}
</script>
