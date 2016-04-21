<template lang="jade">
section.page__wrapper.page--min-height
  .content__wrapper
    .content__section
      .httperror__404
        img.eyes(src="/static/img/icons/action/ic_highlight_off_48px.svg")
        img.eyes(src="/static/img/icons/action/ic_highlight_off_48px.svg")
        br
        img.mouth(src="/static/img/icons/content/ic_remove_48px.svg")
        h2.httperror__message Oops, this page doesn't exist!
        a.button.button--small(v-link="{ name: 'home' }") Go home
</template>

<script>
export default {
}
</script>
