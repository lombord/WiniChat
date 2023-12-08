<template>
  <div class="vol-box">
    <button @click="toggleMute" class="icon-btn vol-btn">
      <span class="flex justify-center w-6">
        <i v-if="muted || !volume" class="fa-solid fa-volume-xmark"></i>
        <i v-else-if="volume <= 20" class="fa-solid fa-volume-off"></i>
        <i v-else-if="volume <= 60" class="fa-solid fa-volume-low"></i>
        <i v-else class="fa-solid fa-volume-high"></i>
      </span>
    </button>
    <RangeSlider v-model="_volume" class="vol-range" :min="0" :max="100" />
  </div>
</template>

<script>
import RangeSlider from "./RangeSlider.vue";

export default {
  props: {
    volume: {
      type: Number,
      required: true,
    },
    toggleMute: {
      type: Function,
      required: true,
    },
    muted: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    _volume: {
      get() {
        return this.volume;
      },
      set(val) {
        this.$emit("update:volume", val);
      },
    },
  },

  components: { RangeSlider },
};
</script>

<style scoped>
.vol-box {
  @apply relative flex justify-center gap-1  items-center;
  --rangeColor: theme(colors.base-content);
}

.vol-range {
  --color1: var(--rangeColor);
  @apply w-14 opacity-0 absolute z-10
  -rotate-90 -translate-y-12 shadow-xl;
}

.vol-box:hover .vol-range {
  @apply opacity-100;
}

.vol-btn {
  @apply p-2 py-2.5 w-10;
}

.vol-range::-webkit-slider-thumb {
  @apply transform-none !important;
}

.vol-range::-moz-range-thumb {
  @apply transform-none !important;
}
</style>
