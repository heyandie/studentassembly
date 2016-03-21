export const initResource = (Vue) => {
  Vue.http.options.root = Vue.config.debug ? 'http://localhost:8000/api' : 'https://studentassembly.herokuapp.com/api'
  Vue.http.interceptors.push({
    request: function(request) {
      var token, headers;

      token = localStorage.getItem('sa-token')
      headers = request.headers || (request.headers = {})

      if (token !== null && token !== 'undefined') {
        headers.Authorization = 'JWT ' + token
      }

      return request
    },
    response: function(response) {
      if (response.status === 401) {
        localStorage.removeItem('sa-token')
      }
      if (response.headers && response.headers.Authorization) {
        localStorage.setItem('sa-token', response.headers.Authorization)
      }
      if (response.data && response.data.token && response.data.token.length > 10) {
        localStorage.setItem('sa-token', response.data.token)
      }

      return response
    }
  })
}
