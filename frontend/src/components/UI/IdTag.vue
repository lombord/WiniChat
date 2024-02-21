<template>
  <IconTag class="text-base-content/75" icon="fa-solid fa-at text-secondary">
    <slot />
  </IconTag>
</template>

<script>
import IconTag from "./IconTag.vue";
export default {
  components: { IconTag },
};
</script>

<style lang="scss" scoped></style>
