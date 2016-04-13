<template lang="jade">
v-header
section.page__wrapper
  .content__wrapper
    .content__section
      article.content__main
        h1 Rating drilldown
</template>

<script>
import Header from '../../components/header.vue'

export default {
  data () {
    return {
      msg: 'yay'
    }
  },
  created () {
    this.$http.get('staff/' + this.$route.params.id).then(
      function (response) {
        console.log(response.data)
      },
      function (response) {
        console.log('Failed to retrieve staff rating.')
      }
    )
  },
  components: {
    'v-header': Header
  }
}
</script>
