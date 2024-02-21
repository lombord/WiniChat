<template>
  <div class="audio-box col-flex">
    <span class="text-primary-medium text-5xl">
      <i class="bi bi-soundwave"></i>
    </span>
    <div
      class="absolute bottom-0 inset-0 p-3 text-center col-flex justify-between"
    >
      <p>{{ file_name }}</p>
      <p class="text-sm">{{ file_size }}</p>
    </div>
  </div>
</template>

<script>
import fileMixin from "@/mixins/fileMixin.js";

export default {
  props: {
    file: {
      type: Object,
      required: true,
    },
  },

  mixins: [fileMixin],
};
</script>

<style scoped>
.audio-box {
  @apply p-14 rounded-2xl bg-base-200/60  
  grid place-content-center
  border-base-content/10 backdrop-blur-xl border;
}
</style>
