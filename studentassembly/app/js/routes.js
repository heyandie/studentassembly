module.exports = {
  configRouter: function (router) {
    router.map({
      '/index': {
        name: 'home',
        component: require('./pages/index.vue')
      },
      '/login': {
        name: 'login',
        component: require('./pages/auth/login.vue')
      },
      '/logout': {
        name: 'logout',
        needAuth: true,
        component: require('./pages/auth/logout.vue')
      },
      '/register': {
        name: 'register',
        component: require('./pages/auth/register.vue')
      },
      '/report': {
        name: 'report',
        needAuth: true,
        component: require('./pages/report.vue')
      },
      '*': {
        component: require('./pages/404.vue')
      }
    });

    router.alias({
      '': '/index',
    });

    router.beforeEach(function (transition) {
      var token = localStorage.getItem('jwt-token');
      if (transition.to.needAuth) {
        if (!token || token === null) {
          transition.redirect('/login');
        }
      }
      if (transition.to.guest) {
        if (token) {
          transition.redirect('/');
        }
      }
      transition.next();
    });
  }
}
