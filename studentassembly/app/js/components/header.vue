<template lang="jade">
header.header__wrapper
  nav.nav__wrapper(role="navigation")
    .nav.nav--left
      a.nav__link.nav--home(v-link="{ name: 'home' }")
        img.nav__logo(src="/static/img/logo-glyph.png", height="32")
      .nav__link.nav--search#search_menu_icon(@click="showSearchBar = !showSearchBar")
        img(v-show="showSearchBar", src="/static/img/icons/navigation/ic_close_24px.svg", height="22")
        img(v-show="!showSearchBar", src="/static/img/icons/action/ic_search_24px.svg", height="22")
      form.nav__search#search_menu_bar(:class="showSearchBar ? 'nav__search--open' : ''")
        input(type="text", tabindex="-1", placeholder="Search Student Assembly", @keydown.enter.prevent="search", @click.stop="true")
    .nav.nav--right
      template(v-if="userID")
        a.nav__link(v-link="{ name: 'report' }") Report
        a.nav__link(v-link="{ name: 'rate' }") Rate
        .nav__link#user_menu(@click="showUserMenu = !showUserMenu", :class="showUserMenu ? 'hovered' : ''")
          v-avatar(:alias="alias", :inline="true", height="24px", width="24px")
          img(src="/static/img/icons/navigation/ic_arrow_drop_down_18px.svg")
          .dropdown__menu(:class="showUserMenu ? 'dropdown__menu--open' : ''")
            .dropdown__menu-header
              span Signed in as&nbsp;
              strong {{ alias }}
            a.dropdown__menu-item(v-link="{ name: 'profile' }") Profile
            a.dropdown__menu-item(v-link="{ name: 'logout' }") Logout

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
      userID: ({ user }) => user.id,
      alias: ({ user }) => user.alias
    },
    actions: {
      getProfile
    }
  },
  data () {
    return {
      showUserMenu: false,
      showSearchBar: false
    }
  },
  methods: {
    search (e) {
      if (e.target.value.length > 0)
        this.$router.go('/search?q=' + e.target.value)
    }
  },
  created () {
    this.getProfile()
  },
  ready () {
    document.addEventListener("keydown", (e) => {
      if (this.showUserMenu && e.keyCode == 27)
        this.showUserMenu = false
      if (this.showSearchBar && e.keyCode == 27)
        this.showSearchBar = false
    })
    document.addEventListener("click", (e) => {
      if (e.target.id !== 'user_menu')
        this.showUserMenu = false
      if (e.target.id !== 'search_menu_icon' && e.target.id !== 'search_menu_bar')
        this.showSearchBar = false
    })
  },
  components: {
    'v-avatar': Avatar
  }
}
</script>
