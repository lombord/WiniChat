<template>
  <input
    ref="input"
    class="input-widget block w-full"
    @keydown.stop
    type="text"
    v-bind="$attrs"
    v-model="value"
  />
</template>

<script>
import inputMixin from "./inputMixin.js";

export default {
  mixins: [inputMixin],
  inheritAttrs: false,
};
</script>

<style scoped></style>
