<template>
  <Modal
    class="modal-box h-full"
    @mousedown.prevent.stop="dragOn"
    @mouseup.prevent.stop="dragOff"
    @mouseleave.prevent.stop="dragOff"
    v-on="isDragging ? { mousemove: moveImg } : {}"
    :style="{ '--sX': `${curX}px`, '--sY': `${curY}px` }"
    :class="dragCls"
  >
    <div class="full-box overflow-hidden pointer-events-none select-none">
      <ImgAnim class="full-screen-img" :src="url" alt="" />
    </div>
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
import ImgAnim from "../ImgAnim.vue";

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
    dragCls() {
      return this.isDragging && ["transition-none", "cursor-move"];
    },
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
      this.curX += e.clientX - this.prevX;
      this.curY += e.clientY - this.prevY;
      this.prevX = e.clientX;
      this.prevY = e.clientY;
    },

    resetAll() {
      this.zoom = 100;
      this.curX = 0;
      this.curY = 0;
    },
  },

  mixins: [fileMixin],
  components: { Modal, ImgAnim },
};
</script>

<style scoped>
:deep(.modal-box) {
  --min-w: 900px;
  --zoom: v-bind(zoom/100);
  --sX: 0;
  --sY: 0;
  @apply p-0 animate-none 
    duration-300
    translate-x-[--sX] 
    translate-y-[--sY]
    scale-[var(--zoom)];
}

.full-box {
  @apply overflow-hidden max-h-[600px];
}

:deep(.full-screen-img) {
  @apply object-contain rounded-3xl 
  w-full object-center
  max-h-[inherit];
}

:deep(.full-screen-img.placeholder) {
  @apply min-w-[300px] min-h-[400px];
}
</style>
