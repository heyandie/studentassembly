var Vue = require('vue');
var VueResource = require('vue-resource');
var VueRouter = require('vue-router');

// Middleware
Vue.use(VueResource);
Vue.use(VueRouter);

// Configure routes
import { configRouter } from './routes';
const router = new VueRouter({
  history: true,
  saveScrollPosition: true
});

// Configure app
window.config = require('./config');
Vue.config.debug = config.env === 'development' ? true : false;

// Configure HTTP client
var rest = require('rest')
var pathPrefix = require('rest/interceptor/pathPrefix')
var mime = require('rest/interceptor/mime')
var defaultRequest = require('rest/interceptor/defaultRequest')
var errorCode = require('rest/interceptor/errorCode')
var interceptor = require('rest/interceptor')
var jwtAuth = require('./interceptors/jwtAuth')

window.client = rest.wrap(pathPrefix, { prefix: config.api.base_url })
                    .wrap(mime)
                    .wrap(defaultRequest, config.api.defaultRequest)
                    .wrap(errorCode, { code: 400 })
                    .wrap(jwtAuth);

// Bootstrap app
configRouter(router);
const App = Vue.extend(require('./app.vue'));
router.start(App, '#app');
