<template>
  <input
    type="checkbox"
    v-model="value"
    :checked="value || fakeCheck"
    ref="input"
    class="toggle toggle-md toggle-check"
  />
</template>

<script>
import inputMixin from "./inputMixin.js";

export default {
  props: {
    fakeCheck: {
      type: Boolean,
      default: false,
    },
  },

  mounted() {
    this.$refs.input.checked = this.value || this.fakeCheck;
  },

  mixins: [inputMixin],
};
</script>

<style scoped>
.toggle-check {
  --active-color: theme(colors.primary-light);
  @apply border-2;
}

.toggle-check:checked,
.toggle-check[checked="true"],
.toggle-check[aria-checked="true"] {
  @apply bg-[--active-color] text-[--active-color] 
  border-[--active-color] !important;
}
</style>
