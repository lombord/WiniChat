<template>
  <div class="search-root">
    <TInput
      class="s-input peer"
      type="search"
      placeholder="Search..."
      v-bind="$attrs"
    />
    <div class="icon-div">
      <i class="fa-solid fa-magnifying-glass"></i>
    </div>
  </div>
</template>

<script>
import TInput from "./TInput.vue";
export default {
  components: { TInput },
  inheritAttrs: false,
};
</script>

<style scoped>
.search-root {
  @apply relative flex items-center text-base;
}

.s-input {
  @apply w-full pl-10
  py-3 h-auto 
  rounded-full;
  font-size: inherit !important;
}

.icon-div {
  @apply absolute left-4
  text-base-content/50
  peer-hover:text-primary-medium
  peer-focus:text-primary-medium;
  font-size: calc(1.2em);
}
</style>
