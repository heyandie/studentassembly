<template lang="jade">
v-header
section.page__wrapper
  .content__wrapper
    .content__section
      .httperror__404
        img.eyes(src="/static/img/icons/action/ic_highlight_off_48px.svg")
        img.eyes(src="/static/img/icons/action/ic_highlight_off_48px.svg")
        br
        img.mouth(src="/static/img/icons/content/ic_remove_48px.svg")
        h2.httperror__message Oops, this page doesn't exist!
        p
          | Go to&nbsp;
          a(v-link="{ name: 'profile' }") my profile
</template>

<script>
import Header from '../components/header.vue'
import Footer from '../components/footer.vue'

export default {
  components: {
    'v-header': Header,
    'v-footer': Footer
  }
}
</script>
