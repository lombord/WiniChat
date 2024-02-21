<template>
  <div class="input-box" :class="wrapCls">
    <slot v-bind="$attrs" :placeholder="pHolder" class="w-full" />
    <span class="input-placeholder">{{ pHolder || "None" }}</span>
  </div>
</template>

<script>
export default {
  props: {
    placeholder: {
      type: String,
    },
    wrapCls: {
      default: null,
    },
  },

  computed: {
    pHolder() {
      return this.placeholder || this.$attrs.name;
    },
  },

  inheritAttrs: false,
};
</script>

<style scoped>
.input-box {
  @apply relative;
}

:deep(.input-widget::placeholder) {
  @apply text-transparent !important;
}

.input-placeholder {
  transition-property: bottom, left, font-size, color;
  @apply absolute  overflow-visible capitalize
  text-base-content/70 font-medium
  ease-in-out duration-150
  p-0 z-10 bg-base-100 
  left-4 bottom-[50%] 
  text-base pointer-events-none;
}

.input-widget:is(:focus, :not(:placeholder-shown)) ~ .input-placeholder {
  @apply bottom-[100%] left-3 text-sm;
}

.input-widget:is(:focus, :hover:not(:placeholder-shown)) ~ .input-placeholder {
  @apply text-primary-light;
}

.input-placeholder {
  @apply leading-[0px] !important;
}

.input-placeholder::before {
  @apply content-[''] absolute 
  translate-y-[25%] -z-10 -inset-[2px]
   inset-x-0 bg-inherit rounded-full;
}
</style>
