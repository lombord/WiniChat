<template>
  <div class="audio-box">
    <button @click="$emit('playAudio')" class="btn play-btn relative">
      <span>
        <i class="fa-solid fa-pause pause-icon"></i>
        <i class="fa-solid fa-play play-icon"></i>
      </span>
      <span
        class="download-btn"
        @click.stop="$session.download(file.url, file_name)"
      >
        <i class="fa-solid fa-circle-down"></i>
      </span>
    </button>
    <div class="overflow-hidden">
      <h6>{{ file_name }}</h6>
      <p class="text-sm font-medium flex gap-2">
        <span>{{ durationFormat }}</span>
        <span>{{ file_size }}</span>
      </p>
    </div>
  </div>
</template>

<script>
import audioMixin from "./audioMixin.js";
export default {
  mixins: [audioMixin],
  emits: ["playAudio"],
};
</script>

<style scoped>
.audio-box {
  @apply flex items-center gap-2 p-3 shadow-sm 
  bg-base-100 rounded-xl overflow-hidden
  text-base-content/80;
}

.play-btn {
  @apply rounded-full px-3 w-12 py-2.5 border-none
  bg-primary-medium text-white text-xl;
}

.download-btn {
  @apply absolute text-base -right-1 -bottom-1 
  px-1 bg-base-100 text-primary-light rounded-full;
}

.pause-icon {
  @apply hidden;
}

.current .pause-icon {
  @apply inline-block;
}
.current .play-icon {
  @apply hidden;
}
</style>
