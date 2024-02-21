<template>
  <div class="tracks-list">
    <TrackItem
      v-for="(file, i) in files"
      :file="file"
      :key="i"
      :class="{
        'current-track': currIdx == i,
        playing: currIdx == i && playing,
      }"
      @click="$emit('playTrack', i)"
    />
  </div>
</template>

<script>
import TrackItem from "./TrackItem.vue";
export default {
  props: {
    files: {
      type: Array,
      required: true,
    },
    currIdx: {
      type: Number,
      required: true,
    },
    playing: {
      type: Boolean,
      required: true,
    },
  },
  emits: ["playTrack"],
  components: { TrackItem },
};
</script>

<style scoped>
.tracks-list {
  @apply max-h-[300px] border 
  pointer-events-auto max-w-sm
  p-1.5 overflow-y-auto flex flex-col 
  gap-1 bg-base-300/60 backdrop-blur-2xl 
  border-base-content/10 rounded-2xl;
}

:deep(.track-box:not(.current-track):hover) {
  @apply bg-base-content/10;
}

.current-track {
  @apply bg-primary-focus/90;
}

.current-track :deep(.play-btn) {
  @apply text-white/[85%];
}

.current-track.playing :deep(.pause-icon) {
  @apply inline-block;
}
.current-track.playing :deep(.play-icon) {
  @apply hidden;
}

.current-track :deep(.track-title) {
  @apply text-white/90;
}

.current-track :deep(.track-author) {
  @apply text-white/60;
}

.current-track :deep(.track-duration) {
  @apply text-white/80;
}
</style>
