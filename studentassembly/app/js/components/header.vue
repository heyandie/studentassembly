<template lang="jade">
header.header__wrapper(:class="headerClass")
  nav.nav__wrapper
    .nav.nav--left
      a(v-link="{ name: 'home' }")
        img.nav__logo(src="/static/img/logo.png" height="54")
    .nav.nav--right
      template(v-if="loggedIn")
        a.nav__link(v-link="{ name: 'report' }") Report
        a.nav__link(v-link="{ name: 'profile' }") Profile
        a.nav__link(v-link="{ name: 'logout' }") Logout
      template(v-else)
        a.nav__link(href="#0") How It Works
        a.nav__link(v-link="{ name: 'login' }") Login
        a.nav__link(v-link="{ name: 'register' }") Register
</template>

<script>
module.exports = {
  props: {
    headerClass: ''
  },
  computed: {
    loggedIn: function() {
      return this.$root.token !== null;
    }
  },
  data: function() {
    return {
      msg: 'Hello'
    }
  }
}
</script>
