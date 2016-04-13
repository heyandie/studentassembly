<template lang="jade">
input(@keydown.enter.prevent="true" type="text" v-bind:name="name" v-bind:placeholder="placeholder")
</template>

<script>
import AutoComplete from '../vendor/autocomplete'

export default {
  props: {
    name: {
      type: String,
      default: 'field'
    },
    placeholder: {
      type: String,
      default: 'Placeholder'
    },
    datalist: {
      type: Array,
      default: function () {
        return ['value']
      }
    }
  },
  data () {
    return {
      autoComplete: null
    }
  },
  watch: {
    'datalist': function (list) {
      let that = this
      this.autoComplete = new AutoComplete({
        selector: that.$el,
        minChars: 0,
        offsetTop: -3,
        source: (term, suggest) => {
          term = term.toLowerCase()
          let matches = []
          for (let i = 0; i < list.length; i++) {
            if (~list[i].name.toLowerCase().indexOf(term))
              matches.push(list[i])
          }
          suggest(matches)
        },
        renderItem: (item, search) => {
          search = search.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&')
          var re = new RegExp("(" + search.split(' ').join('|') + ")", "gi")
          return '<div class="autocomplete-suggestion" data-id="' + item.id + '" data-val="' + item.name + '">' + item.name.replace(re, "<b>$1</b>") + '</div>'
        },
        onSelect: (e, term, item) => {
          that.$dispatch('value', parseInt(item.getAttribute('data-id')))
        }
      })
    }
  },
  beforeDestroy () {
    if (this.autoComplete)
      this.autoComplete.destroy()
  }
}
</script>
