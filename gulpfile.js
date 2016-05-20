var elixir = require('laravel-elixir');

if (elixir.config.production === true) {
  process.env.NODE_ENV = 'production'
}

elixir.config.js.browserify.transformers.push({
  name: 'vueify'
});

elixir.config.js.browserify.watchify = {
    enabled: true,
    options: {
        poll: true
    }
}

elixir(function(mix) {
  mix.sass('./studentassembly/app/sass/app.scss', './static/css/app.css');
  mix.browserify('./studentassembly/app/js/build.js', './static/js/build.js');
});
