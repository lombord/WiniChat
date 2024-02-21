<template>
  <div class="pwd-box">
    <PHInput v-bind="$attrs" :type="inputType" wrapCls="w-full" />
    <button
      type="button"
      @click.stop="show = !show"
      class="icon-btn toggle-btn"
    >
      <i v-if="!show" class="fa-solid fa-eye"></i>
      <i v-else class="fa-solid fa-eye-slash"></i>
    </button>
  </div>
</template>

<script>
import PHInput from "./PHInput.vue";

export default {
  data: () => ({
    show: false,
  }),
  computed: {
    inputType() {
      return this.show ? "text" : "password";
    },
  },
  components: { PHInput },
  inheritAttrs: false,
};
</script>

<style scoped>
.pwd-box {
  @apply relative flex items-center;
}

.toggle-btn {
  @apply absolute right-3 p-0
  opacity-20 bg-transparent;
}

.toggle-btn > * {
  @apply w-7 h-4;
}

.toggle-btn:hover {
  @apply bg-base-content/10 opacity-100 text-primary-light;
}
</style>
