<template lang="jade">
navbar
img(src="/static/img/student.jpg")
h1 {{ msg }}
</template>

<script>
var NavBar = require('../components/navbar.vue');

module.exports = {
  data: function() {
    return {
      msg: 'Hello StudentAssembly with Vue.js'
    }
  },
  components: {
    'navbar': NavBar
  }
}
</script>
