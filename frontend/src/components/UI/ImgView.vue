<template>
  <div :class="$attrs.class" class="img-prev group">
    <img
      class="object-cover object-center max-h-[inherit] max-w-[inherit] w-full h-full"
      :src="url"
      alt=""
    />
    <div class="buttons">
      <button @click="show = true" class="btn">
        <i class="fa-solid fa-eye"></i>
      </button>
      <button
        @click.prevent="$session.download(url, file_name)"
        class="btn text-secondary"
      >
        <i class="fa-solid fa-download"></i>
      </button>
    </div>
  </div>
  <Modal v-model:show="show" class="p-0">
    <div class="overflow-hidden max-h-[600px]">
      <img
        class="object-cover rounded-3xl w-full object-center max-h-[inherit]"
        :src="url"
        alt=""
      />
    </div>
  </Modal>
</template>

<script>
import Modal from "./Modal.vue";

export default {
  data: () => ({
    show: false,
  }),
  props: {
    file: {
      type: Object,
      required: true,
    },
  },
  computed: {
    url() {
      return this.file.url;
    },
    file_name() {
      return this.file.file_name || this.url.split("/").reverse()[0];
    },
  },
  components: { Modal },
};
</script>

<style scoped>
.img-prev {
  @apply overflow-hidden relative
  rounded-2xl cursor-pointer;
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
