<template lang="jade">
footer.footer__wrapper
  nav.nav__wrapper.nav--footer(role="navigation")
    a.nav__link.nav--home(v-link="{ name: 'home' }")
      img.nav__logo(src="/static/img/logo-glyph-white.png", height="24")
    a.nav__link(v-link="{ name: 'about' }") About
    a.nav__link(target="_blank", href="http://www.peoplepowerph.org") 2016 &copy; PPAC
</template>

<script>
export default {
  data () {
    return {
      msg: 'Hello'
    }
  }
}
</script>
