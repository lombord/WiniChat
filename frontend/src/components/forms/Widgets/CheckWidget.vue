<template>
  <div>
    <label :disabled="disabled" class="label input-widget p-3 cursor-pointer">
      <span class="label-text">{{ label }}</span>
      <CheckBox v-bind="$attrs" :disabled="disabled" />
    </label>
  </div>
</template>

<script>
import CheckBox from "./CheckBox.vue";
export default {
  props: {
    label: {
      type: String,
      required: true,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },

  components: { CheckBox },
  inheritAttrs: false,
};
</script>

<style scoped>
.input-widget[disabled]:not([disabled="false"]) * {
  @apply text-base-content/70 !important;
}
</style>
