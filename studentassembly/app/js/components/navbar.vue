<template lang="jade">
nav
  .nav__wrapper
    .nav.nav--left
      a.nav__link(href="#0")
        img.nav__logo(src="/static/img/logo.png" height="40")
    .nav.nav--right
      a.nav__link(href="#0") How It Works
      a.nav__link(href="#0") Partners
      a.nav__link(href="#0") About Us
      a.nav__link(href="#0") Contact Us
</template>

<script>
module.exports = {
  data: function() {
    return {
      msg: 'Hello'
    }
  }
}
</script>
