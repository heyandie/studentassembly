<template lang="jade">
v-header
router-view
//- v-footer
</template>

<script>
import Header from '../../components/header.vue'
import Footer from '../../components/footer.vue'

export default {
  components: {
    'v-header': Header,
    'v-footer': Footer
  }
}
</script>
