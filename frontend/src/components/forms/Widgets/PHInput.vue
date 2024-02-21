<template>
  <PHolderWrap v-slot="scope">
    <TInput v-bind="scope" />
  </PHolderWrap>
</template>

<script>
import TInput from "./TInput.vue";
import PHolderWrap from "./PHolderWrap.vue";
export default {
  components: { TInput, PHolderWrap },
};
</script>

<style scoped></style>
