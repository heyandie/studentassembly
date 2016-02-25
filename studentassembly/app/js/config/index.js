var env = process.env.APP_ENV || 'development'

if (location.host == 'studentassembly.herokuapp.com') {
  env = 'staging';
}

var config = {
  development: require('./development.config'),
  production: require('./production.config'),
  staging: require('./staging.config')
}

module.exports = config[env]
