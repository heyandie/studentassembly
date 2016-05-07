<template lang="jade">
section.page__wrapper.page--min-height
  .content__wrapper
    .content__section
      h2 Results for '{{ $route.query.q }}'

</template>

<script>
export default {
  created () {
    let query = encodeURIComponent(this.$route.query.q).replace(/%20/g, "+")
    this.$http.get('report?q=' + query).then(
      (response) => {
        console.log(response.data)
      },
      (response) => {
        console.log('Failed to retrieve reports')
      }
    )
    this.$http.get('staff?q=' + query).then(
      (response) => {
        console.log(response.data)
      },
      (response) => {
        console.log('Failed to retrieve staff')
      }
    )
  }
}
</script>
