<template>
  <div :class="$attrs.class" class="img-prev group">
    <img class="thumb-img" :src="url" alt="" />
    <div class="buttons">
      <button @click="show = true" class="btn">
        <i class="fa-solid fa-eye"></i>
      </button>
      <button
        @click.prevent="$session.download(url, file_name)"
        class="btn text-secondary"
      >
        <i class="bi bi-cloud-download"></i>
      </button>
    </div>
  </div>
  <Modal v-model:show="show" class="modal-box">
    <div class="full-box">
      <img class="full-img" :src="url" alt="" />
    </div>
    <template #buttons>
      <button v-if="zoom != 100" @click="zoom = 100" class="btn">
        <i class="fa-solid fa-rotate-right"></i>
      </button>
      <button @click="zoomBox(25)" class="btn">
        <i class="bi bi-zoom-in"></i>
      </button>
      <button @click="zoomBox(-25)" class="btn">
        <i class="bi bi-zoom-out"></i>
      </button>
      <button @click="$session.download(url, file_name)" class="btn">
        <i class="bi bi-cloud-download"></i>
      </button>
    </template>
  </Modal>
</template>

<script>
import Modal from "./Modal.vue";
import { ref } from "vue";

export default {
  __zoom: ref(100),

  data: () => ({
    show: false,
    minZoom: 25,
    maxZoom: 300,
  }),

  props: {
    file: {
      type: Object,
      required: true,
    },
  },
  computed: {
    zoom: {
      get() {
        return this.$options.__zoom.value;
      },
      set(val) {
        this.$options.__zoom.value = val;
      },
    },

    url() {
      return this.file.url;
    },
    file_name() {
      return this.file.file_name || this.url.split("/").reverse()[0];
    },
  },

  methods: {
    zoomBox(val) {
      this.zoom = Math.max(
        this.minZoom,
        Math.min(this.zoom + val, this.maxZoom)
      );
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

.thumb-img {
  @apply object-cover object-center 
  max-h-[inherit] max-w-[inherit]
  w-full h-full;
}

:deep(.modal-box) {
  --zoom: v-bind(zoom/100);
  @apply p-0 animate-none transition duration-300;
  transform: scale(var(--zoom));
}

.full-box {
  @apply overflow-hidden max-h-[600px];
}

.full-img {
  @apply object-contain rounded-3xl w-full object-center
    max-h-[inherit];
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
