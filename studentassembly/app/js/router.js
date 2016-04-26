import Vue from 'vue'
import VueRouter from 'vue-router'
import { toTitleCase } from './util'

Vue.use(VueRouter)

const router = new VueRouter({
  history: true,
  saveScrollPosition: true
})

router.map({
  '/index': {
    name: 'home',
    guest: true,
    component: require('./pages/index.vue')
  },
  '/about': {
    name: 'about',
    component: require('./pages/about.vue')
  },
  '/register': {
    name: 'register',
    guest: true,
    component: require('./pages/auth/register.vue')
  },
  '/login': {
    name: 'login',
    guest: true,
    component: require('./pages/auth/login.vue')
  },
  '/logout': {
    name: 'logout',
    component: require('./pages/auth/logout.vue')
  },
  '/profile': {
    name: 'profile',
    needAuth: true,
    component: require('./pages/user/profile.vue')
  },
  '/report': {
    name: 'report',
    component: {
      template: "<router-view></router-view>"
    },
    subRoutes: {
      '/file': {
        name: 'file-a-report',
        needAuth: true,
        component: require('./pages/report/file.vue')
      },
      '/view/:id': {
        name: 'report-view',
        component: require('./pages/report/view.vue')
      }
    }
  },
  '/rate': {
    name: 'rate',
    needAuth: true,
    component: {
      template: "<router-view></router-view>"
    },
    subRoutes: {
      '/staff': {
        name: 'rate-staff',
        component: require('./pages/rating/staff.vue')
      },
      '/view/:id': {
        name: 'rate-view',
        component: require('./pages/rating/view.vue')
      }
    }
  },
  '*': {
    component: require('./pages/404.vue')
  }
})

router.alias({
  '': '/index',
  '/report': '/report/file',
  '/rate': '/rate/staff'
})

router.beforeEach((transition) => {
  let token = localStorage.getItem('sa-token')

  if (transition.to.needAuth) {
    if (!token || token === null) {
      transition.redirect('/login')
    }
    else {
      let tokenObject = JSON.parse(atob(token.split('.')[1])),
          timeRemaining = tokenObject.exp - Math.floor(Date.now() / 1000)

      if (timeRemaining < 10) {
        transition.redirect('/logout?s=expired')
      }

      // if (timeRemaining > 10 && timeRemaining < 300) {
      //   transition.redirect('/refresh_token')
      // }
    }
  }
  if (transition.to.guest) {
    if (token) {
      transition.redirect('/profile')
    }
  }

  transition.next()
})

router.afterEach((transition) => {
  let title = transition.to.name || 'page-not-found'
  document.title = 'Student Assembly - ' + toTitleCase(title)
  window.scrollTo(0, 0)
})

export default router
