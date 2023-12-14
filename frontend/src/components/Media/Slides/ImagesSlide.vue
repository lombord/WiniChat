<template>
  <div class="images-box dynamic-flex">
    <div
      @click="showSlide(i)"
      class="img-box group"
      v-for="(file, i) in files"
      :key="i"
    >
      <ImgAnim class="full-img prev-img" :src="file.url" />
      <div class="buttons">
        <button class="btn">
          <i class="fa-solid fa-eye"></i>
        </button>
      </div>
    </div>
  </div>
  <MediaSlide
    modal="ImgModalView"
    :files="files"
    v-model:index="currIdx"
    v-model:show="show"
  />
</template>

<script>
import parentMixin from "./parentMixin.js";
import ImgAnim from "../ImgAnim.vue";

export default {
  mixins: [parentMixin],
  components: { ImgAnim },
};
</script>

<style scoped>
.images-box > * {
  @apply relative cursor-pointer bg-base-100;
}

.buttons {
  @apply hidden absolute inset-0 
  bg-black/20 backdrop-blur-sm 
  justify-center gap-2 p-2 px-4
  group-hover:flex flex-col;
}

.buttons > * {
  @apply bg-transparent text-2xl p-0
  text-white opacity-70 border-none;
}
</style>
