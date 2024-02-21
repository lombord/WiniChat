<template>
  <div class="edit-box">
    <p class="center-content edit-icon-wrap">
      <i class="fa-solid fa-pen"></i>
    </p>
    <div class="truncate flex-1">
      {{ content }}
    </div>
    <button @click="$emit('cancel')" class="icon-btn p-3">
      <i class="fa-solid fa-xmark"></i>
    </button>
  </div>
</template>

<script>
export default {
  props: {
    content: {
      type: String,
      required: true,
    },
  },

  emits: ["cancel"],
};
</script>

<style scoped>
.edit-box {
  @apply p-1.5 px-2.5 flex gap-2 items-center 
  bg-base-200/70 border border-base-content/10 
  backdrop-blur-xl w-full rounded-2xl relative;
}

.edit-icon-wrap {
  @apply text-primary-medium rounded-full aspect-square p-3.5
  bg-base-200/40 text-xl border border-base-content/20;
}
</style>
