<template lang="jade">
input(
  type="text",
  :name="name",
  :placeholder="placeholder",
  @keydown.enter.prevent="true",
  @input="dispatchIfEmpty"
)
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
    initValue: {
      type: String,
      default: ''
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
          for (let i = 0; i < list.length; i++)
            if (~list[i].name.toLowerCase().indexOf(term)) matches.push(list[i])
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

      // datalist won't be present if declared as a separate watch
      if (this.initValue.length)
        this.prefillInput()
    }
  },
  methods: {
    dispatchIfEmpty (e) {
      if (e.target.value.length < 1)
        this.$dispatch('value', null)
    },
    prefillInput () {
      let data = this.datalist.find((v) => { return v.name.toLowerCase() === this.initValue.toLowerCase() })
      this.$el.value = data.name || ''
      this.$dispatch('value', data.id || 0)
    }
  },
  beforeDestroy () {
    if (this.autoComplete)
      this.autoComplete.destroy()
  }
}
</script>
