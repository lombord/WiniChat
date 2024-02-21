<template>
  <div class="wrapper-box center-content">
    <Transition name="pop" mode="out-in">
      <button v-show="show" @click="$emit('scrolled')" class="btn to-bottom">
        <span v-show="unread" class="unread-badge">
          {{ unread }}
        </span>
        <i class="fa-solid fa-chevron-down"></i>
      </button>
    </Transition>
  </div>
</template>

<script>
export default {
  props: {
    unread: {
      type: Number,
      required: true,
    },
    show: {
      type: Boolean,
      required: true,
    },
  },
  emits: ["scrolled"],
};
</script>

<style scoped>
.wrapper-box {
  @apply sticky bottom-[6.8rem] inset-x-0 h-0
  pointer-events-none grid place-content-center z-10;
}

.unread-badge {
  @apply absolute -top-2 text-base aspect-square 
  h-6 grid content-center p-1 bg-secondary rounded-full;
}
.to-bottom {
  @apply bg-primary-medium text-white py-4
  rounded-full opacity-60 aspect-square
  relative outline-none border-none
  pointer-events-auto
  hover:opacity-100 btn-square;
}
</style>
