<template lang="jade">
header.header__wrapper(:class="headerClass")
  nav.nav__wrapper
    .nav.nav--left
      a(v-link="{ name: 'home' }")
        img.nav__logo(src="/static/img/logo.png" height="54")
    .nav.nav--right
      a.nav__link(href="#0") How It Works
      a.nav__link(v-link="{ name: 'login' }") Login
      a.nav__link(v-link="{ name: 'register' }") Register
      //- a.nav__link(href="#0") Contact
</template>

<script>
module.exports = {
  props: {
    headerClass: ''
  },
  data: function() {
    return {
      msg: 'Hello'
    }
  }
}
</script>
