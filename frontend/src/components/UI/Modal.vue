<template>
  <Transition name="modal">
    <div v-if="show" class="modal-root">
      <div
        :class="rootCls"
        class="modal-wrap"
        @click="$emit('update:show', false)"
      >
        <div
          :class="$attrs.class"
          class="modal-content"
          @click.stop
          @mousedown.stop
        >
          <slot> </slot>
        </div>
      </div>
      <div class="buttons-wrap">
        <div class="buttons-box">
          <slot name="buttons"></slot>
          <button @click="$emit('update:show', false)" class="btn">
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
  cursor-pointer
  min-h-screen;
}

.buttons-wrap {
  @apply absolute right-2 top-2 bottom-0 pointer-events-none;
}

.buttons-box {
  @apply flex gap-2 
  items-center sticky top-2
  pointer-events-auto;
}

.close-btn {
  @apply py-3.5 btn-square text-lg rounded-full text-white
  btn-outline opacity-80 hover:opacity-100;
}

.buttons-box > *,
.buttons-box > :deep(*) {
  @apply close-btn;
}

.modal-content {
  @apply p-3 transition rounded-3xl
  overflow-hidden
  cursor-auto
  max-h-[700px]
  max-w-2xl bg-base-100 
  w-[min(600px,100%)]
  min-h-[200px];
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
