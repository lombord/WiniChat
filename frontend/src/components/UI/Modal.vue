<template>
  <!-- Modal Placeholder -->
  <Transition name="modal">
    <div ref="modalElm" v-show="show" class="modal-root">
      <div
        :class="rootCls"
        class="modal-wrap"
        @click="$emit('update:show', false)"
      >
        <div @click.stop @mousedown.stop v-bind="$attrs" class="modal-content">
          <slot> </slot>
        </div>
      </div>
      <slot name="contentOut"></slot>
      <div class="buttons-wrap">
        <div class="buttons-box">
          <slot name="buttons"></slot>
          <button @click="$emit('update:show', false)" class="modal-btn">
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script>
export default {
  props: {
    show: {
      type: Boolean,
      required: true,
    },
    rootCls: {
      type: String,
      default: "center-content",
    },
  },

  computed: {
    modalElm() {
      return this.$refs.modalElm;
    },
    modalsElm() {
      return document.getElementById("modals");
    },
  },

  mounted() {
    this.teleportNode();
  },

  activated() {
    this.teleportNode();
  },

  beforeUnmount() {
    this.clearNode();
  },

  deactivated() {
    this.clearNode();
  },

  methods: {
    teleportNode() {
      this.modalsElm.appendChild(this.modalElm);
    },
    clearNode() {
      if (this.modalElm.isConnected) {
        this.modalsElm.removeChild(this.modalElm);
      }
    },
  },
  mixins: ["update:show"],
  inheritAttrs: false,
};
</script>

<style scoped>
.modal-root {
  @apply fixed inset-0 z-[1000] 
  overflow-hidden overflow-y-auto;
}
.modal-wrap {
  @apply bg-slate-800/60
  backdrop-blur-[1px] p-3 sm:p-4
  relative
  min-h-screen;
}

.buttons-wrap {
  @apply fixed right-2 top-2 pointer-events-none;
}

.buttons-box {
  @apply flex gap-2 flex-wrap
  items-center justify-end
  pointer-events-auto;
}

.modal-content {
  --min-w: 600px;
  @apply p-3 transition rounded-3xl
  overflow-hidden
  cursor-auto
  max-h-[700px]
  max-w-2xl bg-base-100 
  w-[min(var(--min-w),_100%)];
  animation: 0.15s ease-out 0s 1 zoom;
}

@keyframes zoom {
  0% {
    transform: scale(0.95);
  }
  100% {
    transform: scale(1);
  }
}

.modal-leave-active {
  @apply transition;
}

.modal-leave-to {
  @apply opacity-0;
}
</style>
