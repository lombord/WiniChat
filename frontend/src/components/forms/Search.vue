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
  @apply relative flex items-center -z-10;
}

.s-input {
  @apply w-full pl-10
  py-2.5 h-auto 
  rounded-full !important;
}

.icon-div {
  @apply absolute text-xl left-4
  text-base-content/50
  peer-hover:text-primary
  peer-focus:text-primary;
}
</style>
