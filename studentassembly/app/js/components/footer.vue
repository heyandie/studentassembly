<template lang="jade">
footer.footer__wrapper
  nav.nav__wrapper(role="navigation")
    a.nav__link(v-link="{ name: 'about' }") About
    a.nav__link(target="_blank", href="http://www.peoplepowerph.org") 2016 &copy; People Power Against Corruption
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
