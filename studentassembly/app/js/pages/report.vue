<template lang="jade">
v-header
section.page__wrapper
  .content__wrapper
    .content__section
      h1 Test
</template>

<script>
var Header = require('../components/header.vue');
var Spinner = require('../elements/spinner.vue');

module.exports = {
  data: function() {
    return {
      msg: 'Create an account',
    }
  },
  methods: {
  },
  components: {
    'v-header': Header,
    'v-spinner': Spinner
  }
}
</script>
