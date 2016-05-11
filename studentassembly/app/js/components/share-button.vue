<template lang="jade">
.button.button--tiny.button--simple#share_menu(@click="openShareMenu = !openShareMenu")
  span.u-c-facebook •
  span.u-c-twitter •
  span.u-c-brand •
  .dropdown__menu(v-bind:class="openShareMenu ? 'dropdown__menu--open' : ''")
    .dropdown__menu-header
      span Share
    a.dropdown__menu-item(@click.prevent="shareToFacebook")
      img.button__icon(src="/static/img/fb-logo.png", height="15")
      span Facebook
    a.dropdown__menu-item(@click.prevent="shareToTwitter")
      img.button__icon(src="/static/img/twitter-logo.png", height="14")
      span Twitter
</template>

<script>
export default {
  props: ['type', 'typeId'],
  data () {
    return {
      openShareMenu: false
    }
  },
  computed: {
    typeLink () {
      return 'https://studentassembly.herokuapp.com/' +
              this.type + '/view/' + this.typeId
    }
  },
  methods: {
    shareToFacebook () {
      let link = 'https://facebook.com/sharer/sharer.php?u=' +
                  encodeURIComponent(this.typeLink)
      this.openShareWindow(link)
    },
    shareToTwitter () {
      let link = 'https://twitter.com/intent/tweet?text=' +
                  encodeURIComponent(
                    'Sharing this ' +
                    (this.type === 'report' ? 'report' : 'rating') +
                    ' from Student Assembly. ' + this.typeLink
                  )
      this.openShareWindow(link)
    },
    openShareWindow (url, width = 570, height = 370) {
      let left = (screen.width / 2) - (width / 2),
          top = (screen.height / 2) - (height / 2) - 80
      window.open(url, '',
        'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,width=' +
        width + ',height=' + height + ',top=' + top + ',left=' + left
      )
    }
  },
  ready () {
    document.addEventListener('keydown', (e) => {
      if (this.openShareMenu && e.keyCode == 27)
        this.openShareMenu = false
    })
    document.addEventListener('click', (e) => {
      if (e.target.id !== 'share_menu')
        this.openShareMenu = false
    })
  }
}
</script>
