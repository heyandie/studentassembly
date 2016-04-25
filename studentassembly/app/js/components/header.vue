<template lang="jade">
header.header__wrapper
  nav.nav__wrapper(role="navigation")
    .nav.nav--left
      a.nav__link.nav--home(v-link="{ name: 'home' }")
        img.nav__logo(src="/static/img/logo-glyph.png" height="32")
      form.nav__search
        input(type="text" tabindex="-1" placeholder="Search Student Assembly" @keydown.enter.prevent="search")
    .nav.nav--right
      template(v-if="userId")
        a.nav__link(v-link="{ name: 'report' }") Report
        a.nav__link(v-link="{ name: 'rate' }") Rate
        .nav__link#user_menu(@click="openUserMenu = !openUserMenu")
          v-avatar(v-bind:alias="alias" v-bind:inline="true" height="24px" width="24px")
          img(src="/static/img/icons/navigation/ic_arrow_drop_down_18px.svg")
          .nav__link-menu(v-bind:class="openUserMenu ? 'nav__link-menu--open' : ''")
            a.nav__link-menu-item(v-link="{ name: 'profile' }") Profile
            a.nav__link-menu-item(v-link="{ name: 'logout' }") Logout

      template(v-else)
        a.nav__link(v-link="{ name: 'about' }") About
        a.nav__link(v-link="{ name: 'login' }") Login
        a.nav__link(v-link="{ name: 'register' }") Register
</template>

<script>
import Avatar from '../components/avatar.vue'
import { getProfile } from '../vuex/actions/user'

export default {
  vuex: {
    getters: {
      userId: ({ user }) => user.id,
      alias: ({ user }) => user.alias
    },
    actions: {
      getProfile
    }
  },
  data () {
    return {
      openUserMenu: false
    }
  },
  methods: {
    search (e) {
      this.$router.go('/search?q=' + e.target.value)
    }
  },
  created () {
    this.getProfile()
  },
  ready () {
    document.addEventListener("keydown", (e) => {
      if (this.openUserMenu && e.keyCode == 27)
        this.openUserMenu = false
    })
    document.addEventListener("click", (e) => {
      console.log(e.target.id)
      if (e.target.id !== 'user_menu')
        this.openUserMenu = false
    })
  },
  components: {
    'v-avatar': Avatar
  }
}
</script>
