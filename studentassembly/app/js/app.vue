<template lang="jade">
div
  v-header(:class="$route.name === 'home' ? 'header--landing' : ''")
  router-view
  v-footer
</template>

<script>
import Header from './components/header.vue'
import Footer from './components/footer.vue'
import store from './vuex/store'

export default {
  store,
  components: {
    'v-header': Header,
    'v-footer': Footer
  }
}
</script>
