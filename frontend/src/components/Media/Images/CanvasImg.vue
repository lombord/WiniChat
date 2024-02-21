<template>
  <div class="canvas-img-box" :class="boxCls">
    <ImgAnim @load="drawImage" v-bind="$attrs" class="canvas-img" />
    <canvas ref="canvas" class="canvas-elm"> </canvas>
  </div>
</template>

<script>
export default {
  props: {
    boxCls: {
      default: "",
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

  methods: {
    drawImage({ currentTarget: imgElm }) {
      this.canvas.width = imgElm.naturalWidth;
      this.canvas.height = imgElm.naturalHeight;
      this.context.drawImage(imgElm, 0, 0);
    },
  },

  inheritAttrs: false,
};
</script>

<style scoped>
.canvas-img-box {
  @apply relative z-10;
}

.canvas-img-box :deep(.canvas-img) {
  @apply w-full h-full max-h-[inherit]
  max-w-[inherit]
  object-contain object-center;
}

.canvas-elm {
  @apply absolute inset-0 -z-10 w-full h-full
  brightness-[0.95]
  object-center object-cover blur-lg scale-110;
}
</style>
