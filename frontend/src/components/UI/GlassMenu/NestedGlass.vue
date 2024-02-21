<template>
  <div
    class="nested-menu-box"
    @mouseenter="mouseOver = true"
    @focusin="focused = true"
    @focusout="focused = false"
    @mouseleave="mouseOver = false"
  >
    <GlassBtn :option="option">
      <span>
        <i class="fa-solid fa-chevron-right"></i>
      </span>
    </GlassBtn>
    <slot />
  </div>
</template>

<script>
import GlassBtn from "./GlassBtn.vue";

export default {
  data: () => ({
    mouseOver: false,
    focused: false,
  }),

  props: {
    option: {
      type: Object,
      required: true,
    },
  },

  computed: {
    hoverShow() {
      return this.mouseOver || this.focused;
    },
  },

  created() {
    this.option.hoverShow = false;
  },

  watch: {
    hoverShow(val) {
      this.option.hoverShow = val;
    },
  },

  components: { GlassBtn },
};
</script>

<style scoped>
.nested-menu-box {
  @apply relative flex items-start;
}

:deep(.nested-menu) {
  @apply absolute -right-[calc(100%_+_0.5rem)] z-[1] origin-top-left !important;
}

/* .nested-menu-box:is(:hover, :focus, :active) > :slotted(.nested-menu) {
  @apply block !important;
} */
</style>
