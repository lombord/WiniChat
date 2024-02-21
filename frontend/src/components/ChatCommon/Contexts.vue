<template>
  <ContextWrapper
    v-for="{ owner, messages, uuid } in contexts"
    :key="uuid"
    :messages="messages"
    :owner="owner"
    v-bind="$attrs"
  />
</template>

<script>
import ContextWrapper from "./ContextWrapper.vue";
export default {
  props: {
    contexts: {
      type: Array,
      required: true,
    },
  },

  inheritAttrs: false,
  components: { ContextWrapper },
};
</script>

<style scoped></style>
