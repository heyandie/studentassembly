import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const router = new VueRouter({
  history: true,
  saveScrollPosition: true
})

router.map({
  '/index': {
    name: 'home',
    component: require('./pages/index.vue')
  },
  '/register': {
    name: 'register',
    component: require('./pages/auth/register.vue')
  },
  '/login': {
    name: 'login',
    component: require('./pages/auth/login.vue'),
    subRoutes: {
      '/verified': {
        component: require('./pages/auth/verified.vue')
      }
    }
  },
  '/logout': {
    name: 'logout',
    needAuth: true,
    component: require('./pages/auth/logout.vue')
  },
  '/profile': {
    name: 'profile',
    needAuth: true,
    component: require('./pages/user/profile.vue')
  },
  '/report': {
    name: 'report',
    component: require('./pages/report/index.vue'),
    subRoutes: {
      '/file': {
        name: 'report-file',
        needAuth: true,
        component: require('./pages/report/file.vue')
      },
      '/view/:id': {
        name: 'report-view',
        component: require('./pages/report/view.vue')
      }
    }
  },
  '*': {
    component: require('./pages/404.vue')
  }
})

router.alias({
  '': '/index',
  '/report': '/report/file'
})

router.beforeEach(function (transition) {
  if (transition.to.needAuth) {
    let token = localStorage.getItem('sa-token')
    if (!token || token === null) {
      transition.redirect('/login')
    }
    else {
      let tokenObject = JSON.parse(atob(token.split('.')[1])),
          timeRemaining = tokenObject.exp - Math.floor(Date.now() / 1000)
      if (timeRemaining < 10) {
        // 10 seconds
        transition.redirect('/logout')
      }
    }
  }

  transition.next()
})

export default router
