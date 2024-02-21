<template>
  <div class="images-box dynamic-flex">
    <BlurryImg
      @click="showSlide(i)"
      v-for="(file, i) in files"
      :key="i"
      :url="file.url"
    />
  </div>
  <MediaSlide
    v-if="show"
    modal="ImgModalView"
    :files="files"
    v-model:index="currIdx"
    v-model:show="show"
  />
</template>

<script>
import parentMixin from "./parentMixin.js";
import BlurryImg from "../Images/BlurryImg.vue";

export default {
  mixins: [parentMixin],
  components: { BlurryImg },
};
</script>

<style scoped></style>
