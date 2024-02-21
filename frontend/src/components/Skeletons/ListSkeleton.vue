<template>
  <div class="col-flex sk-flex">
    <div v-for="i in count" :key="i" class="sk-item">
      <slot></slot>
    </div>
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
.sk-flex {
  --min-w: 500px;
  --min-h: 70px;
  @apply grid;
  grid-template-columns: minmax(min(var(--min-w), 100%), 1fr);
}

.sk-item {
  @apply animate-pulse bg-base-100 
  p-2.5 px-3 rounded-3xl min-h-[--min-h];
}
</style>
