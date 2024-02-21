<template>
  <button
    class="option-box col-flex items-center justify-center"
    :class="option.cls"
    @click="triggerCB"
  >
    <div class="icon-box">
      <i :class="option.icon"></i>
    </div>
    <div>
      <h6 class="option-label">{{ option.label }}</h6>
    </div>
  </button>
</template>

<script>
export default {
  props: {
    option: {
      type: Object,
      required: true,
    },
  },

  methods: {
    async triggerCB({ currentTarget: elm }) {
      try {
        elm.classList.add("load-anim");
        await this.option.cb();
      } catch (error) {
        this.$emit(
          "chosen",
          this.option.value || this.option.label.toLowerCase()
        );
      } finally {
        elm.classList.remove("load-anim");
      }
    },
  },

  emits: ["chosen"],
};
</script>

<style scoped>
.option-box {
  --active-color: theme(colors.primary-medium);
  --active-font-color: theme(colors.white/90%);
  --font-color: theme(colors.base-content/95%);
  @apply gap-1 text-center w-full transition-transform
    text-[var(--font-color)]
    cursor-pointer p-4 bg-base-300/80 rounded-2xl;
  transform: translate3d(0, 0, 0);
  backface-visibility: hidden;
}

.option-label {
  @apply text-[var(--font-color)];
}

.option-box.load-anim {
  @apply bg-[var(--active-color)];
}

.option-box.load-anim::after {
  @apply text-[var(--active-font-color)]
  loading-spinner;
}

.option-box:active {
  transform: translate3d(0, 0, 0) scale(0.95);
}

.option-box:is(:hover, :active, :focus) {
  @apply bg-[var(--active-color)];
}

.option-box:is(:hover, :active, :focus) * {
  @apply text-[var(--active-font-color)] !important;
}

.icon-box {
  @apply px-2 text-4xl text-[var(--active-color)];
}
</style>
