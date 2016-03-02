<script>
var Store = require('../../store');

module.exports = {
  route: {
    activate: function (transition) {
      this.$dispatch('userHasLoggedOut');
      transition.redirect('/');
    }
  }
}
</script>
