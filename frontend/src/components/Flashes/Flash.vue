<template>
  <div class="m-alert" :class="`alert-${flash.code}`">
    <p>{{ flash.message }}</p>
    <button class="a-btn" @click="$emit('remove', flash.id)">
      <i class="fa-solid fa-xmark"></i>
    </button>
  </div>
</template>

<script>
export default {
  props: {
    flash: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>
.m-alert {
  @apply py-3 justify-between flex items-start alert
  text-white rounded-md
  pointer-events-auto gap-2;
}

.alert-success {
  @apply bg-success;
}
.alert-info {
  @apply bg-info;
}
.alert-warning {
  @apply bg-warning;
}
.alert-error {
  @apply bg-rose-600;
}

.m-alert {
  @apply bg-opacity-90;
}

.a-btn {
  @apply btn px-2.5 btn-sm rounded-3xl
  btn-ghost hover:bg-white/30;
}
</style>
