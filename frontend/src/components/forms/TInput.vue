<template>
  <input
    class="input"
    @keydown.stop
    type="text"
    :placeholder="$attrs.placeholder || $attrs.name"
    v-model="value"
  />
</template>

<script>
export default {
  props: {
    modelValue: {
      required: true,
    },
  },
  beforeMount() {},
  computed: {
    value: {
      get() {
        return this.modelValue;
      },
      set(newValue) {
        this.$emit("update:modelValue", newValue);
      },
    },
  },
};
</script>

<style scoped>
.input {
  @apply bg-base-100 placeholder:capitalize 
  outline outline-2
  focus:cursor-text
  cursor-pointer
  outline-base-content/10
  focus:outline-primary/80
  hover:outline-primary/80;
}

.input[disabled] {
  @apply outline cursor-auto 
  bg-base-200 outline-base-300
  text-base-content/60;
}

.input {
  @apply outline-offset-0 !important;
}
</style>
