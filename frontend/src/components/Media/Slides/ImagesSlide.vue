<template>
  <div class="images-box dynamic-grid">
    <div
      @click="showSlide(i)"
      class="img-box group"
      v-for="(file, i) in files"
      :key="i"
    >
      <img class="full-img prev-img" :src="file.url" />
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

export default {
  mixins: [parentMixin],
};
</script>

<style scoped>

.images-box > * {
  @apply relative cursor-pointer;
}

.buttons {
  @apply hidden absolute inset-0 
  bg-black/20 backdrop-blur-sm 
  justify-center gap-2 p-2 px-4
  group-hover:flex flex-col;
}

.buttons > * {
  @apply bg-white/60 opacity-80 
  active:bg-white/50 text-lg md:py-4
  text-primary
  hover:opacity-100 border-none;
}
</style>
