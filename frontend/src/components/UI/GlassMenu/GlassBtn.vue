<template>
  <button class="glass-btn" :class="option.cls">
    <span
      class="glass-icon spinner-on-load"
      :class="{ 'load-anim': option.loading }"
    >
      <i :class="option.icon || 'fa-solid fa-circle'"></i>
    </span>
    <span class="flex-1 text-start truncate">
      {{ option.label }}
    </span>
    <slot />
  </button>
</template>

<script>
export default {
  expose: ["$refs"],
  props: {
    option: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>
.glass-btn {
  @apply w-full flex p-1.5 px-4
  transition text-base-content/90
  items-center gap-3 rounded-[14px];
}

.glass-btn {
  animation: glass-pop 200ms theme("transitionTimingFunction.in-out") 1
    backwards;
}

@keyframes glass-pop {
  0% {
    transform: scale(0);
    opacity: 0;
  }

  100% {
    transform: none;
    opacity: 1;
  }
}

.glass-btn:active {
  @apply scale-95;
}

.glass-btn:hover {
  @apply bg-base-content/10;
}

.glass-icon {
  @apply w-4 text-center overflow-visible;
}
</style>
