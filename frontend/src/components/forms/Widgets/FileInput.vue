<template>
  <input
    v-bind="$attrs"
    ref="fileInput"
    @input="changed"
    class="hidden"
    hidden
    type="file"
  />
  <slot :callback="selectFile"> </slot>
</template>

<script>
export default {
  methods: {
    selectFile() {
      const ev = new MouseEvent("click");
      this.$refs.fileInput.dispatchEvent(ev);
    },
    changed(e) {
      this.$emit("selected", e.target.files);
    },
  },
  inheritAttrs: false,
};
</script>

<style scoped></style>
