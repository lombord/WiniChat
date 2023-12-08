<template>
  <div class="audio-box">
    <i class="bi bi-soundwave"></i>
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
};
</script>

<style scoped>
.audio-box {
  @apply p-14 rounded-2xl bg-base-200/60 text-primary 
  grid place-content-center
  border-base-content/10 backdrop-blur-xl border text-5xl;
}
</style>
