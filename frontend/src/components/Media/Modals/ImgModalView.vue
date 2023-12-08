<template>
  <Modal class="modal-box">
    <div class="full-box">
      <img class="full-screen-img" :src="url" alt="" />
    </div>
    <template #buttons>
      <button v-if="zoom != 100" @click="zoom = 100" class="modal-btn">
        <i class="fa-solid fa-rotate-right"></i>
      </button>
      <button @click="zoomBox(25)" class="modal-btn">
        <i class="bi bi-zoom-in"></i>
      </button>
      <button @click="zoomBox(-25)" class="modal-btn">
        <i class="bi bi-zoom-out"></i>
      </button>
      <button @click="$session.download(url, file_name)" class="modal-btn">
        <i class="bi bi-cloud-download"></i>
      </button>
    </template>
    <template #contentOut>
      <slot name="contentOut"></slot>
    </template>
  </Modal>
</template>

<script>
import { ref } from "vue";
import Modal from "@/components/UI/Modal.vue";
import fileMixin from "@/mixins/fileMixin.js";

export default {
  __zoom: ref(100),

  data: () => ({
    minZoom: 25,
    maxZoom: 300,
  }),

  computed: {
    zoom: {
      get() {
        return this.$options.__zoom.value;
      },
      set(val) {
        this.$options.__zoom.value = val;
      },
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

  mixins: [fileMixin],
  components: { Modal },
};
</script>

<style scoped>
:deep(.modal-box) {
  --min-w: 900px;
  --zoom: v-bind(zoom/100);
  @apply p-0 animate-none transition duration-300;
  transform: scale(var(--zoom));
}

.full-box {
  @apply overflow-hidden max-h-[600px];
}

.full-screen-img {
  @apply object-contain rounded-3xl w-full object-center
    max-h-[inherit];
}
</style>
