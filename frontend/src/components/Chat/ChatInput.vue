<template>
  <div class="input-box">
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
  @apply text-center p-2 pt-0 bg-base-200/50
  pt-1
  z-20 relative;
}

/* .input-box::before {
  @apply content-[''] bg-base-200/5
  absolute inset-x-0 pt-3 z-10 top-0
  -translate-y-3
  backdrop-blur-sm;
} */

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
