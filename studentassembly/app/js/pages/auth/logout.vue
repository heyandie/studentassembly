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

      let query = ''
      if (transition.to.query.r === 'expired')
        query = '?s=expired'

      transition.redirect('/login' + query)
    }
  }
}
</script>
