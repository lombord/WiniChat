<template>
  <div class="overlay-box">
    <ImgView :file="{ url }" class="full-img" />
    <div class="overlay-content">
      <slot />
    </div>
  </div>
</template>

<script>
import ImgView from "./ImgView.vue";

export default {
  props: {
    url: {
      type: String,
      required: true,
    },
  },
  components: { ImgView },
};
</script>

<style scoped>
.overlay-box {
  @apply rounded-2xl overflow-hidden h-72
  backdrop-blur-0 relative flex-shrink-0;
}

.overlay-box::before {
  content: "";
  @apply absolute z-10 pointer-events-none
  inset-0;
  background: rgb(0, 0, 0);
  background: linear-gradient(
    0deg,
    rgba(0, 0, 0, 0.731) 5%,
    rgba(255, 255, 255, 0) 35%
  );
}

.overlay-content {
  @apply absolute z-10 bottom-3.5 left-4;
}
</style>
