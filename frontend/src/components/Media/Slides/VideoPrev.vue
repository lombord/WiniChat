<template>
  <div class="video-box">
    <video
      ref="video"
      class="full-img object-contain"
      muted
      @loadedmetadata="rewindVideo"
      @seeked="setCVImage"
      :src="file.url"
    />
    <canvas ref="canvas" class="video-cv"></canvas>
    <div class="video-overlay">
      <button class="icon-btn text-white text-3xl px-3.5">
        <i class="fa-solid fa-play"></i>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    file: {
      type: Object,
      required: true,
    },
  },

  computed: {
    
    video() {
      return this.$refs.video;
    },

    canvas() {
      return this.$refs.canvas;
    },

    ctx() {
      return this.canvas.getContext("2d");
    },
  },

  methods: {
    rewindVideo({ target }) {
      target.currentTime = target.duration / 2;
      this.canvas.width = target.videoWidth;
      this.canvas.height = target.videoHeight;
    },
    setCVImage({ target }) {
      this.ctx.drawImage(target, 0, 0);
    },
  },
};
</script>

<style scoped>
.video-box {
  @apply bg-black
  overflow-hidden blur-0 backdrop-blur-0
  relative cursor-pointer;
}

.video-overlay {
  @apply bg-opacity-0 transition-colors
  duration-[350ms] grid 
  place-content-center
  absolute inset-0 z-10;
}

.video-cv {
  @apply absolute -z-10 inset-0 
  w-full h-full overflow-hidden
  object-fill object-top blur-xl scale-110;
}
</style>
