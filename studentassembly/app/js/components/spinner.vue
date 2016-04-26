<template lang="jade">
  .spinner(:style="dimensions")
    svg.circular(:style="dimensions")
      circle.path(
        :class="onButton ? 'path--button' : ''",
        :cx="radius",
        :cy="radius",
        :r="radius",
        fill="none",
        stroke-miterlimit="10",
        :stroke-width="strokeWidth",
        :style="pathStyle"
      )
</template>

<script>
export default {
  props: {
    onButton: {
      type: Boolean,
      default: false
    },
    color: {
      type: String,
      default: '#ff5f2e'
    },
    strokeWidth: {
      type: String,
      default: '2'
    },
    radius: {
      type: String,
      default: '20'
    }
  },
  data () {
    return {
      dimensions: {
        overflow: 'visible',
      	height: Math.ceil(parseInt(this.radius) * 2) + 'px',
     		width: Math.ceil(parseInt(this.radius) * 2) + 'px'
      },
      pathStyle: {
        stroke: this.color,
        strokeDasharray: '1,' + Math.ceil(parseInt(this.radius) * 2 * 3.14),
        strokeDashoffset: '0'
      }
    }
  },
  computed: {
    diameter () {
      this.radius
    }
  }
}
</script>

<style lang="scss">
.spinner {
  margin: 0 auto;

  & + h3, & + h4 {
    margin-top: 16px;
  }
}

.circular{
  position: relative;
  animation: rotate 2s linear infinite;
}

.path {
  animation: dash 1.5s ease-in-out infinite;
  stroke-linecap: round;

  &.path--button {
    animation: dash-button 1.5s ease-in-out infinite;
  }
}

@keyframes rotate{
  100%{
    transform: rotate(360deg);
  }
}
@keyframes dash{
  0%{
    stroke-dasharray: 1, 125;
    stroke-dashoffset: 0;
  }
  50%{
    stroke-dasharray: 94, 125;
    stroke-dashoffset: -32;
  }
  100%{
    stroke-dasharray: 94, 125;
    stroke-dashoffset: -125;
  }
}
@keyframes dash-button{
  0%{
    stroke-dasharray: 1, 44;
    stroke-dashoffset: 0;
  }
  50%{
    stroke-dasharray: 33, 44;
    stroke-dashoffset: -11;
  }
  100%{
    stroke-dasharray: 33, 44;
    stroke-dashoffset: -44;
  }
}
</style>
