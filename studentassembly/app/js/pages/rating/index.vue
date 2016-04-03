<template lang="jade">
v-header
router-view
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
              strong {{ key }}
              span &nbsp;{{ val }}

//- v-footer
</template>

<script>
import Header from '../../components/header.vue'
import Footer from '../../components/footer.vue'

export default {
  data () {
    return {
      staff: []
    }
  },
  components: {
    'v-header': Header,
    'v-footer': Footer
  },
  created () {
    this.$http.get('staff').then(
      function(response) {
        this.staff = response.data
        console.log(response.data)
      },
      function(response) {
        console.log(response)
      }
    )
  }
}
</script>
