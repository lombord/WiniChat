<template>
  <div class="dynamic-flex">
    <div
      class="video-box"
      @click="showSlide(i)"
      v-for="(file, i) in files"
      :key="i"
    >
      <video
        class="full-img backdrop-blur-sm"
        muted
        @timeupdate="checkRange"
        @loadedmetadata="rewindVideo"
        :src="file.url"
      />
      <div class="video-overlay">
        <button class="icon-btn text-white text-3xl px-3.5">
          <i class="fa-solid fa-play"></i>
        </button>
      </div>
    </div>
  </div>
  <MediaSlide
    modal="VideoModalView"
    :files="files"
    v-model:index="currIdx"
    v-model:show="show"
  />
</template>

<script>
import parentMixin from "./parentMixin.js";

export default {
  methods: {
    rewindVideo({ target }) {
      target.currentTime = target.duration / 2;
    },
    checkRange({ target }) {},
  },

  mixins: [parentMixin],
};
</script>

<style scoped>
.video-box {
  @apply bg-black relative cursor-pointer;
}

.video-overlay {
  @apply transition-colors
  duration-[250] grid place-content-center
  absolute inset-0 z-10;
}

.video-box:hover .video-overlay {
  @apply bg-base-300/10 
  backdrop-blur-lg;
}
</style>
