<template>
  <div class="m-alert" :class="`alert-${flash.code}`">
    <div>{{ flash.message }}</div>
    <button class="a-btn" @click="$emit('remove')">
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
  rounded-md relative overflow-hidden bg-transparent
  text-white/90 outline-none border-none
  pointer-events-auto gap-2;
  --bg-color: theme(colors.info);
}

.m-alert::before {
  @apply content-[''] absolute inset-0 
  -z-10 bg-[--bg-color] backdrop-blur brightness-[1.1];
}

.alert-success {
  --bg-color: theme(colors.success/70%);
}
.alert-info {
  --bg-color: theme(colors.info/70%);
}
.alert-warning {
  --bg-color: theme(colors.warning/70%);
}
.alert-error {
  --bg-color: theme(colors.error/70%);
}

.a-btn {
  @apply btn px-2.5 btn-sm rounded-3xl
  btn-ghost hover:bg-white/30;
}
</style>
