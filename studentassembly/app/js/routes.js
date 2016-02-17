module.exports = {
  configRouter: function (router) {
    router.map({
      '/index': {
        name: 'home',
        component: require('./pages/index.vue')
      },
      '/login': {
        name: 'login',
        component: require('./pages/login.vue')
      },
      '/register': {
        name: 'register',
        component: require('./pages/register.vue')
      },
      '*': {
        component: require('./pages/404.vue')
      }
    });

    router.alias({
      '': '/index',
    });
  }
}
