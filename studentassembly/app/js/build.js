window.Vue = require('vue');
window.VueRouter = require('vue-router');

import { configRouter } from './routes';
const router = new VueRouter({
  history: true,
  saveScrollPosition: true
});
configRouter(router);

const App = Vue.extend(require('./app.vue'));
router.start(App, '#app');
window.router = router;
