<template>
  <div class="input-box">
    <slot name="top"></slot>
    <form class="s-form">
      <TInput
        v-bind="$attrs"
        class="s-input peer"
        placeholder="Type Something..."
      />
      <button class="s-btn" type="submit" :class="{ 'text-primary': iVal }">
        <i class="fa-solid fa-arrow-up"></i>
      </button>
    </form>
  </div>
</template>

<script>
import TInput from "@/components/forms/TInput.vue";

export default {
  components: { TInput },
  computed: {
    iVal() {
      return !!this.$attrs.modelValue;
    },
  },
};
</script>

<style scoped>
.input-box {
  @apply text-center p-2 py-2.5 bg-base-100/30
  backdrop-blur-2xl sticky bottom-0
  z-10 relative;
}

.s-form {
  @apply relative flex items-center 
  max-w-4xl mx-auto;
}

.s-input {
  @apply w-full;
}
.s-btn {
  @apply absolute right-3 py-3
  invisible
  rounded-full min-h-fit h-fit
  btn btn-ghost text-lg outline-0
  text-base-content/50
  peer-focus:visible;
}
</style>
