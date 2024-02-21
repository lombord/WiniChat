<template>
  <RangeSlider
    :min="0"
    :max="duration"
    step="0.1"
    :style="{ '--buffered': buffered }"
    class="media-range"
  />
</template>

<script>
import RangeSlider from "./RangeSlider.vue";

export default {
  props: {
    duration: {
      type: Number,
      required: true,
    },
    buffered: {
      type: Number,
      required: true,
    },
  },

  components: { RangeSlider },
};
</script>

<style scoped>
.media-range {
  @apply w-full;
  --color2: theme(colors.white / 90%);
  --color3: theme(colors.white/ 60%);
  --buffered: 0;
  background: linear-gradient(
    to right,
    var(--color1) calc(var(--percent) * 1% + 2px),
    var(--color2) calc(var(--percent) * 1%) calc(var(--buffered) * 1%),
    var(--color3) calc(var(--buffered) * 1%)
  );
}
</style>
