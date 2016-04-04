<template lang="jade">
header.header__wrapper(:class="headerClass")
  nav.nav__wrapper(role="navigation")
    .nav.nav--left
      a.nav__link.nav--home(v-link="{ name: 'home' }")
        img.nav__logo(src="/static/img/logo-glyph.png" height="32")
      form.nav__search
        input(type="text" tabindex="-1" placeholder="Search for reports or people")

    .nav.nav--right
      template(v-if="loggedIn")
        a.nav__link(v-link="{ name: 'report' }") Report
        a.nav__link(v-link="{ name: 'rate' }") Rate
        a.nav__link(v-link="{ name: 'profile' }") Profile
        a.nav__link(v-link="{ name: 'logout' }") Logout
      template(v-else)
        a.nav__link(v-link="{ name: 'about' }") About
        a.nav__link(v-link="{ name: 'login' }") Login
        a.nav__link(v-link="{ name: 'register' }") Register
</template>

<script>
export default {
  props: {
    headerClass: ''
  },
  computed: {
    loggedIn () {
      return localStorage.getItem('sa-token') !== null
    }
  }
}
</script>
