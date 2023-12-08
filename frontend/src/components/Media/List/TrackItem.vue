<template>
  <div class="track-box">
    <button class="play-btn center-content">
      <i class="fa-solid fa-pause pause-icon"></i>
      <i class="fa-solid fa-play play-icon"></i>
    </button>
    <div class="flex-1 overflow-hidden">
      <h6 class="track-title">
        {{ title }}
      </h6>
      <p class="track-author">
        {{ author }}
      </p>
    </div>
    <p class="track-duration">
      {{ durationFormat }}
    </p>
  </div>
</template>

<script>
import audioMixin from "./audioMixin.js";
export default {
  mixins: [audioMixin],
};
</script>

<style scoped>
.track-box {
  @apply p-1 px-4 flex items-center gap-3 rounded-xl cursor-pointer;
}

.play-btn {
  @apply text-primary w-4 text-lg;
}

.pause-icon {
  @apply hidden;
}

.track-title,
.track-author {
  @apply capitalize;
}
</style>
