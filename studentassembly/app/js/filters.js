import Vue from 'vue'
import RelativeDate from 'relative-date'

function capitalizeFirstLetter (str) {
  let smallWords = /^(a|an|and|as|at|but|by|en|for|if|in|nor|of|on|or|per|the|to|vs?\.?|via)$/

  if (!smallWords.test(str))
    return str.charAt(0).toUpperCase() + str.slice(1)
  else
    return str
}

export const registerFilters = () => {
  Vue.filter('relativeDate', (date) => {
    return RelativeDate(Date.parse(date))
  })

  Vue.filter('toDateString', (date) => {
    return new Date(date).toDateString()
  })

  Vue.filter('truncate', (string, limit = 140) => {
    if (string.length > limit)
      return string.substring(0, limit) + '...'
    else
      return string
  })

  Vue.filter('nl2br', (text) => {
    return String(text).replace(/\n\n/g, "<div class='u-mg-b-12'></div>")
  })

  Vue.filter('toTitleCase', (string, sep = '-') => {
    return string.split(sep).map((text) => {
      return capitalizeFirstLetter(text)
    }).join(' ')
  })

  // Vue.filter('currencyDisplay', {
  //   // model -> view
  //   // formats the value when updating the input element.
  //   read: function(val) {
  //     return '$'+val.toFixed(2)
  //   },
  //   // view -> model
  //   // formats the value when writing to the data.
  //   write: function(val, oldVal) {
  //     var number = +val.replace(/[^\d.]/g, '')
  //     return isNaN(number) ? 0 : parseFloat(number.toFixed(2))
  //   }
  // })

}
