<template>
  <div class="p-bubble">
    <div class="bubble-img-box" @click="$emit('remove', person)">
      <ImgAnim class="round-img w-8 scale-105" :src="person.photo" />
      <div class="uncheck">
        <i class="fa-solid fa-xmark uncheck-icon"></i>
      </div>
    </div>
    <p class="pr-2 flex-1">
      {{ person.username }}
    </p>
  </div>
</template>

<script>
export default {
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  emits: ["remove"],
};
</script>

<style scoped>
.p-bubble {
  @apply flex items-center gap-2 max-w-[150px]
  bg-primary rounded-full overflow-visible text-white/90;
}

.bubble-img-box {
  @apply flex-none relative rounded-full
  cursor-pointer;
}

.uncheck {
  @apply absolute scale-0 -inset-[1px] rounded-full
  transition grid place-content-center
  bg-secondary text-white text-xl;
}

.uncheck-icon {
  @apply transition;
}

.uncheck:active .uncheck-icon {
  @apply scale-[0.85];
}

.p-bubble:hover .uncheck {
  @apply scale-105;
}
</style>
