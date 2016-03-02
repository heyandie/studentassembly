<template lang="jade">
v-header
section.page__wrapper
  .content__wrapper
    .content__section
      h1 Profile
      h3 Hello, {{ username }}!
</template>

<script>
var Header = require('../components/header.vue');
var Spinner = require('../components/spinner.vue');

module.exports = {
  data: function() {
    return {
      username: null
    }
  },
  methods: {
  },
  ready: function() {
    var that = this;
    client({ path: 'user' }).then(
      function (response) {
        try {
          that.username = response.entity.username;
        }
        catch (e) {
          console.log(e);
        }
      },
      function (response) {
        // Fail
      }
    );
  },
  components: {
    'v-header': Header,
    'v-spinner': Spinner
  }
}
</script>
