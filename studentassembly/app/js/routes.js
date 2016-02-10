module.exports = {
  configRouter: function (router) {
    router.map({
      '/index': {
        component: require('./pages/index.vue')
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
