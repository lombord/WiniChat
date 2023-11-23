<template>
  <div class="root-box">
    <button class="btn toggle-btn" @click="toggleState">
      <span class="w-3 flex justify-center">
        <i v-if="ended" class="fa-solid fa-rotate-right"></i>
        <i v-else-if="loading" class="fa-solid fa-spinner fa-spin-pulse"></i>
        <i v-else-if="paused" class="fa-solid fa-play"></i>
        <i v-else class="fa-solid fa-pause"></i>
      </span>
    </button>
    <MediaSlider
      @input="updateCurrent"
      :buffered="buffered"
      :duration="duration"
      v-model="currentTime"
      class="video-range"
    />
    <div class="text-sm w-16 truncate text-clip">
      {{ currentFormat }}
    </div>
    <div class="vol-box">
      <button @click="toggleMute" class="icon-btn p-2 py-2.5">
        <span class="flex justify-center w-6">
          <i v-if="muted || !volume" class="fa-solid fa-volume-xmark"></i>
          <i v-else-if="volume <= 20" class="fa-solid fa-volume-off"></i>
          <i v-else-if="volume <= 60" class="fa-solid fa-volume-low"></i>
          <i v-else class="fa-solid fa-volume-high"></i>
        </span>
      </button>
      <RangeSlider v-model="volume" class="vol-range" :min="0" :max="100" />
    </div>
    <audio
      @play="paused = false"
      @pause="paused = true"
      @timeupdate="timeChanged"
      @durationchange="durationChanged"
      @volumechange="volumeChanged"
      @progress="calcProgress"
      @seeking="loading = true"
      @waiting="loading = true"
      @loadeddata="loading = false"
      @playing="loading = false"
      @seeked="loading = false"
      ref="mediaElm"
      class="audio-tag hidden"
      :src="src"
    />
  </div>
</template>

<script>
import MediaView from "./MediaView.vue";
import MediaSlider from "./MediaSlider.vue";
import RangeSlider from "./RangeSlider.vue";

export default {
  extends: MediaView,
  components: { MediaSlider, RangeSlider },
};
</script>

<style scoped>
.root-box {
  @apply flex items-center p-3 gap-2 
  bg-base-200 rounded-2xl md:w-[350px]
  text-base-content/80 shadow;
}

.toggle-btn {
  @apply btn-primary rounded-full px-3.5 py-3;
}

.video-range {
  --color2: theme(colors.base-content/50%);
  --color3: theme(colors.base-content/30%);
  @apply shadow flex-1;
}
.vol-box {
  @apply relative flex justify-center gap-1 mr-1 items-center;
}

.vol-range {
  @apply w-14 opacity-0 absolute 
  -rotate-90 -translate-y-12 shadow-xl;
  --color1: theme(colors.base-content);
}

.vol-box:hover .vol-range {
  @apply opacity-100;
}
.vol-range::-webkit-slider-thumb {
  @apply transform-none !important;
}

.vol-range::-moz-range-thumb {
  @apply transform-none !important;
}
</style>
