<template>
  <Modal
    class="modal-box h-full"
    @mousedown.prevent.stop="dragOn"
    @mouseup.prevent.stop="dragOff"
    @mouseleave.prevent.stop="dragOff"
    @mousemove.prevent.stop="moveImg"
    :class="{ 'modal-drag': isDragging }"
  >
    <CanvasImg
      boxCls="modal-img-box"
      class="modal-img"
      loading="eager"
      :src="url"
    />
    <template #buttons>
      <button
        v-if="zoom != 100 || curX || curY"
        @click="resetAll"
        class="modal-btn"
      >
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
import CanvasImg from "../Images/CanvasImg.vue";

function genPropFor(name) {
  return {
    get() {
      return this.$options[name].value;
    },
    set(val) {
      this.$options[name].value = val;
    },
  };
}

export default {
  __zoom: ref(100),
  __curX: ref(0),
  __curY: ref(0),

  data: () => ({
    minZoom: 25,
    maxZoom: 300,

    prevX: 0,
    prevY: 0,
    isDragging: false,
  }),

  computed: {
    zoom: genPropFor("__zoom"),
    curX: genPropFor("__curX"),
    curY: genPropFor("__curY"),
  },

  methods: {
    zoomBox(val) {
      this.zoom = Math.max(
        this.minZoom,
        Math.min(this.zoom + val, this.maxZoom)
      );
    },
    dragOn(e) {
      this.prevX = e.clientX;
      this.prevY = e.clientY;
      this.isDragging = true;
    },
    dragOff(e) {
      this.isDragging = false;
    },
    moveImg(e) {
      if (this.isDragging) {
        this.curX += e.clientX - this.prevX;
        this.curY += e.clientY - this.prevY;
        this.prevX = e.clientX;
        this.prevY = e.clientY;
      }
    },

    resetAll() {
      this.zoom = 100;
      this.curX = 0;
      this.curY = 0;
    },
  },

  mixins: [fileMixin],
  components: { Modal, CanvasImg },
};
</script>

<style scoped>
:deep(.modal-box) {
  --min-w: 900px;
  --zoom: v-bind(zoom/100);
  --sX: calc(v-bind(curX) * 1px);
  --sY: calc(v-bind(curY) * 1px);
  @apply p-0 animate-none 
    relative bg-transparent
    backdrop-blur-0
    shadow-none
    translate-x-[--sX] 
    translate-y-[--sY]
    scale-[var(--zoom)];
}

:deep(.modal-box.modal-drag) {
  @apply transition-none cursor-move;
}

.modal-root {
  @apply overflow-y-hidden;
}

.modal-img-box {
  @apply overflow-hidden max-h-[600px]
  pointer-events-none select-none;
}

.modal-img-box :deep(.img-placeholder) {
  @apply min-w-[300px] min-h-[400px] bg-base-100;
}
</style>
