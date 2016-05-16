<script>
import { logout } from '../../vuex/actions/auth'

export default {
  vuex: {
    actions: {
      logout
    }
  },
  route: {
    activate (transition) {
      this.logout()
    }
  }
}
</script>
