<template>
  <div @click="show = true" :class="$attrs.class" class="img-prev group">
    <img class="thumb-img" :src="url" alt="" />
    <div class="buttons">
      <button class="btn">
        <i class="fa-solid fa-eye"></i>
      </button>
      <slot v-if="showOpButtons" name="buttons" :file="file">
        <button
          @click.prevent="$session.download(url, file_name)"
          class="btn text-secondary"
        >
          <i class="bi bi-cloud-download"></i>
        </button>
      </slot>
    </div>
  </div>
  <ImgModalView v-model:show="show" :file="file" />
</template>

<script>
import ImgModalView from "./Modals/ImgModalView.vue";
import fileMixin from "@/mixins/fileMixin.js";

export default {
  data: () => ({
    show: false,
  }),

  props: {
    showOpButtons: {
      type: Boolean,
      default: true,
    },
  },

  mixins: [fileMixin],
  components: { ImgModalView },
};
</script>

<style scoped>
.img-prev {
  @apply overflow-hidden relative cursor-pointer;
}

.thumb-img {
  @apply object-cover object-center 
  max-h-[inherit] max-w-[inherit]
  w-full h-full;
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
