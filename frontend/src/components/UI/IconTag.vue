<template>
  <p class="icon-tag-box">
    <i :class="icon"></i>
    <slot />
  </p>
</template>

<script>
export default {
  props: {
    icon: {
      default: "",
    },
  },
};
</script>

<style scoped>
.icon-tag-box {
  @apply text-base-content/75 flex font-bold 
  items-center gap-[3px];
}
</style>
