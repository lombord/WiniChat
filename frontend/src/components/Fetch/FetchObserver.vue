<template>
  <div>
    <div v-if="hasTop" class="observer-box">
      <div class="load-anim observer"></div>
      <div
        v-int="fetchTop"
        :class="topCls"
        class="top-full invisible-observer"
      ></div>
    </div>
    <slot />
    <div v-if="hasBottom" class="observer-box">
      <div
        v-int="fetchBottom"
        :class="bottomCls"
        class="invisible-observer bottom-full"
      ></div>
      <div class="load-anim observer"></div>
    </div>
  </div>
</template>

<script>
export default {
  expose: ["$el"],

  props: {
    hasTop: {
      type: Boolean,
      default: false,
    },
    hasBottom: {
      type: Boolean,
      default: false,
    },
    fetchTop: {
      type: Function,
      default: null,
    },
    fetchBottom: {
      type: Function,
      default: null,
    },
    topCls: {
      type: [String, Object, Array],
      default: null,
    },
    bottomCls: {
      type: [String, Object, Array],
      default: null,
    },
  },
};
</script>

<style scoped>
.observer-box {
  @apply h-12 relative z-10 py-2;
}

.observer {
  @apply h-full;
}

.observer.load-anim::after {
  @apply loading-spinner;
}
.invisible-observer {
  @apply absolute inset-x-0 h-[400px] pointer-events-none;
}
</style>
