<template>
  <Transition name="modal">
    <div
      v-if="show"
      class="modal-root center-content"
      @click="$emit('update:show', false)"
    >
      <div :class="$attrs.class" class="modal-box" @click.stop>
        <slot> </slot>
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
  },
  inheritAttrs: false,
};
</script>

<style scoped>
.modal-root {
  @apply fixed inset-0 bg-slate-800/60
  backdrop-blur-[1px]
  overflow-y-auto z-[999];
}

.modal-box {
  @apply p-4 max-h-[min(600px,100vh)] 
  max-w-2xl min-h-[min(200px,100%)] !important;
}

.modal-leave-active {
  @apply transition;
}

.modal-leave-to {
  @apply opacity-0;
}
</style>
