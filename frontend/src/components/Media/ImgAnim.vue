<template>
  <div :class="$attrs.class" v-if="!loaded" class="placeholder load-anim"></div>
  <img v-show="loaded" v-bind="$attrs" @load="loaded = true" />
</template>

<script>
export default {
  data: () => ({
    loaded: false,
  }),

  inheritAttrs: false,
};
</script>

<style scoped>
.placeholder {
  @apply after:loading-ring w-full h-full;
}
</style>
