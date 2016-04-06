import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

function capitalizeFirstLetter(string) {
  let smallWords = /^(a|an|and|as|at|but|by|en|for|if|in|nor|of|on|or|per|the|to|vs?\.?|via)$/

  if (!smallWords.test(string))
    return string.charAt(0).toUpperCase() + string.slice(1)
  else
    return string
}

function toTitleCase(string) {
  return string.split('-').map((text) => { return capitalizeFirstLetter(text) }).join(' ')
}

const router = new VueRouter({
  history: true,
  saveScrollPosition: true
})

router.map({
  '/index': {
    name: 'home',
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
    component: require('./pages/report/index.vue'),
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
    component: require('./pages/rating/index.vue'),
    needAuth: true,
    subRoutes: {
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
  '/report': '/report/file'
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
        // 10 seconds
        transition.redirect('/logout?s=expired')
      }
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
  document.title = 'Student Assembly - ' + toTitleCase(transition.to.name)
})

export default router
