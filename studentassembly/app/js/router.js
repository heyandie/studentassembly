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
    needAuth: true,
    component: require('./pages/report.vue')
  },
  '*': {
    component: require('./pages/404.vue')
  }
})

router.alias({
  '': '/index'
})

router.beforeEach(function (transition) {
  if (transition.to.needAuth) {
    var token = localStorage.getItem('sa-token')
    if (!token || token === null) {
      transition.redirect('/login')
    }
  }

  transition.next()
})

export default router
