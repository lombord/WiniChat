<template>
  <div class="root">
    <TInput v-bind="$attrs" :type="inputType" />
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
import TInput from "./TInput.vue";

export default {
  data: () => ({
    show: false,
  }),
  computed: {
    inputType() {
      return this.show ? "text" : "password";
    },
  },
  components: { TInput },
  inheritAttrs: false,
};
</script>

<style scoped>
.root {
  @apply relative flex items-center;
}

.toggle-btn {
  @apply absolute right-3 p-1 w-7 opacity-20 hover:opacity-100 hover:text-primary;
}
</style>
