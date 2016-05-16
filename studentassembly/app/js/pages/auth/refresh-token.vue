<script>
import { refreshToken } from '../../vuex/actions/auth'

export default {
  vuex: {
    actions: {
      refreshToken
    }
  },
  route: {
    activate (transition) {
      const redir = this.$router._prevTransition
      this.refreshToken(this, redir)
    }
  }
}
</script>
