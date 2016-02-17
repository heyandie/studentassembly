<template lang="jade">
v-header(header-class="header--landing")
section.page__wrapper
  .landing__wrapper
    .landing__overlay
    .landing__content
      h1
        | You deserve
        br
        | to be heard.
      p Student Assembly empowers students to increase transparency and accountability on their schools.
      a.button.button--inverted File a Report
  .content__wrapper
    .content__section
      h1 {{ msg }}
</template>

<script>
var Header = require('../components/header.vue');

module.exports = {
  data: function() {
    return {
      msg: 'Hello StudentAssembly with Vue.js'
    }
  },
  components: {
    'v-header': Header
  }
}
</script>
