<template>
  <div class="dynamic-flex">
    <VideoPrev
      @click="showSlide(i)"
      v-for="(file, i) in files"
      :key="i"
      :file="file"
    />
  </div>
  <MediaSlide
    v-if="show"
    modal="VideoModalView"
    :files="files"
    v-model:index="currIdx"
    v-model:show="show"
  />
</template>

<script>
import parentMixin from "./parentMixin.js";
import VideoPrev from "./VideoPrev.vue";

export default {
  methods: {},

  components: { VideoPrev },
  mixins: [parentMixin],
};
</script>

<style scoped></style>
