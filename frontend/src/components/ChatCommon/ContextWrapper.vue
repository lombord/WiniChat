<template>
  <Transition name="context" mode="out-in">
    <Context :messages="messages" v-if="messages.length" />
  </Transition>
</template>

<script>
import Context from "./Context.vue";
export default {
  props: {
    messages: {
      type: Array,
      required: true,
    },
  },
  components: { Context },
};
</script>

<style scoped>
.context-enter-active,
.context-leave-active {
  @apply transition;
}

.context-enter-active,
.context-leave-active {
  @apply opacity-0;
}

.context-enter-from {
  transform: translateY(1rem);
}

.context-leave-to:has(.chat-end) {
  transform: translateX(1rem);
}

.context-leave-to:has(.chat-start) {
  transform: translateX(-1rem);
}
</style>
