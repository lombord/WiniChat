<template>
  <div class="dynamic-flex">
    <div v-for="i in count" :key="i" class="skeleton-item"></div>
  </div>
</template>

<script>
export default {
  props: {
    count: {
      type: Number,
      default: 10,
    },
  },
};
</script>

<style scoped>
.skeleton-item {
  @apply animate-pulse 
  bg-base-100 h-[300px];
}
</style>
