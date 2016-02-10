var elixir = require('laravel-elixir');

elixir.config.js.browserify.transformers.push({
  name: 'vueify'
});

elixir(function(mix) {
  mix.sass('./studentassembly/app/sass/app.scss', './static/css/app.css');
  mix.browserify('./studentassembly/app/js/build.js', './static/js/build.js');
});
