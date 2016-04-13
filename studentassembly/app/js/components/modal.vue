<template lang="jade">
.modal-mask(v-show="show" transition="modal")
  .modal-wrapper(@click="show = false")
    .modal-container(@click.stop="true")
      slot(name="content")
</template>

<script>
export default {
  props: {
    show: {
      type: Boolean,
      required: true,
      twoWay: true
    }
  },
  ready () {
    document.addEventListener("keydown", (e) => {
      if (this.show && e.keyCode == 27)
        this.show = false
    })
  }
}
</script>
