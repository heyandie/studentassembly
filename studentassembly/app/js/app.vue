<template>
<div>
  <router-view></router-view>
</div>
</template>

<script>
// TEMPORARY STATE MANAGEMENT; WAITING FOR NPM RELEASE OF VUEX 0.4.0
module.exports = {
  data: function() {
    return {
      token: null
    }
  },
  methods: {
    setLogin: function() {
      this.token = localStorage.getItem('jwt-token');
    },
    destroyLogin: function() {
      this.token = null;
      localStorage.removeItem('jwt-token');
    }
  },
  ready: function() {
    this.$on('userHasLoggedIn', function () {
      this.setLogin();
    });
    this.$on('userHasLoggedOut', function () {
      this.destroyLogin();
    });

    var token = localStorage.getItem('jwt-token');
    if (token !== null && token !== 'undefined') {
      this.setLogin();
    }
  }
}
</script>
