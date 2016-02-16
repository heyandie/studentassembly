<template lang="jade">
header.header__wrapper(:class="headerClass")
  nav.nav__wrapper
    .nav.nav--left
      a(href="#0")
        img.nav__logo(src="/static/img/logo.png" height="54")
    .nav.nav--right
      a.nav__link(href="#0") How It Works
      a.nav__link(href="#0") Login
      //- a.nav__link(href="#0") About
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
