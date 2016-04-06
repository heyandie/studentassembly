<template lang="jade">
.profile__avatar(v-bind:style="containerStyle") {{ alias.charAt(0) }}
</template>

<script>

export default {
  props: {
    alias: {
      type: String,
      default: 'alias'
    },
    height: {
      type: String,
      default: '54px'
    },
    width: {
      type: String,
      default: '54px'
    }
  },
  computed: {
    containerStyle () {
      return {
        margin: '0 auto 12px auto',
        height: this.height,
        width: this.width,
        backgroundColor: this.avatarColor,
        textAlign: 'center',
        fontSize: this.fontSize,
        fontWeight: '500',
        color: '#fff',
        lineHeight: '1.8',
        borderRadius: '50%',
        pointerEvents: 'none',
        userSelect: 'none'
      }
    },
    fontSize () {
      return (parseInt(this.height.replace('px', '')) / 1.6875) + 'px'
    },
    avatarColor () {
      return this.stringToColour(this.alias)
    }
  },
  methods: {
    stringToColour (str) {
      // str to hash
      for (var i = 0, hash = 0; i < str.length; hash = str.charCodeAt(i++) + ((hash << 5) - hash));
      // int/hash to hex
      for (var i = 0, colour = "#"; i < 3; colour += ("00" + ((hash >> i++ * 8) & 0xFF).toString(16)).slice(-2));
      return colour
    }
  }
}
</script>
