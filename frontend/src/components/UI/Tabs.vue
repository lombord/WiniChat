<template>
  <div class="tabs-box">
    <div
      :class="{ 'active-tab': modelValue == val }"
      @click="$emit('update:modelValue', val)"
      v-for="({label, val }) in tabs"
    >
      <slot :name="val">
        {{ label }}
      </slot>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    tabs: {
      type: Array,
      required: true,
    },
    modelValue: {
      required: true,
    },
  },

  emits: ["update:modelValue"],
};
</script>

<style scoped>
.tabs-box {
  @apply grid gap-2 grid-cols-[repeat(auto-fit,_minmax(0,_1fr))]
  bg-base-300 p-2 rounded-xl;
}

.tabs-box > * {
  @apply text-center cursor-pointer 
  py-2 rounded-xl opacity-60 capitalize;
}

.tabs-box > *:not(.active-tab) {
  @apply hover:bg-base-100 hover:opacity-100;
}

.active-tab {
  @apply opacity-100 bg-primary/80 text-white;
}
</style>
