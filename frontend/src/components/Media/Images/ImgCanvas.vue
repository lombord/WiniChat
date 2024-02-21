<template>
  <canvas ref="canvas"> </canvas>
</template>

<script>
export default {
  props: {
    imgElm: {
      type: HTMLImageElement,
      required: true,
    },
  },

  computed: {
    /**
     * @return {HTMLCanvasElement}
     */
    canvas() {
      return this.$refs.canvas;
    },

    /**
     * @return {CanvasRenderingContext2D}
     */
    context() {
      return this.canvas.getContext("2d");
    },
  },

  mounted() {
    if (this.imgElm.complete) {
      this.drawImage({ target: this.imgElm });
    }
    this.imgElm.addEventListener("load", this.drawImage);
  },

  methods: {
    drawImage({ target }) {
      this.canvas.width = target.naturalWidth;
      this.canvas.height = target.naturalHeight;
      this.context.drawImage(target, 0, 0);
    },
  },
};
</script>

<style scoped></style>
