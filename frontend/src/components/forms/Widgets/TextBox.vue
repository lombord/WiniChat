<template>
  <PHolderWrap v-slot="scope">
    <textarea
      ref="input"
      v-model="value"
      v-bind="scope"
      class="text-box input-widget"
      placeholder="Bio"
    ></textarea>
  </PHolderWrap>
</template>

<script>
import inputMixin from "./inputMixin.js";
import PHolderWrap from "./PHolderWrap.vue";
export default {
  mixins: [inputMixin],

  components: { PHolderWrap },
};
</script>

<style scoped>
.text-box {
  @apply max-h-[400px] min-h-[100px] h-[150px] max-w-full block;
}
</style>
