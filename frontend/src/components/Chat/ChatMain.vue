<template>
  <div class="this-is-chat">
    <slot />
  </div>
</template>

<script>
export default {
  props: {
    chat: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped></style>
