<template>
  <component v-if="tag" :is="tag">
    <slot />
  </component>
  <slot v-else />
</template>

<script>
export default {
  name: "TagComp",
  props: {
    tag: {
      type: String,
      default: null,
    },
  },
};
</script>

<style scoped></style>
