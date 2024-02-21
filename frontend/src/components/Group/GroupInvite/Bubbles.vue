<template>
  <div ref="scrollElm" class="tflex overflow-y-auto max-h-[80px] p-1">
    <TransitionGroup name="bubble">
      <Bubble
        v-for="[id, person] in people"
        :key="id"
        v-bind="$attrs"
        :person="person"
      />
    </TransitionGroup>
    <button @click="$emit('clear')" class="btn btn-secondary rounded-full py-2">
      Clear
    </button>
  </div>
</template>

<script>
import Bubble from "./Bubble.vue";

export default {
  props: {
    people: {
      type: Map,
      required: true,
    },
  },

  computed: {
    scrollElm() {
      return this.$refs.scrollElm;
    },
  },

  watch: {
    "people.size": {
      async handler(a, b) {
        if (a > b) {
          await this.$nextTick();
          this.scrollElm.scrollTo({ top: this.scrollElm.scrollHeight });
        }
      },
      deep: true,
    },
  },
  emits: ["clear"],
  inheritAttrs: false,
  components: { Bubble },
};
</script>

<style scoped>
.bubble-enter-active,
.bubble-leave-active {
  @apply transition;
}

.bubble-enter-from,
.bubble-leave-to {
  @apply opacity-0 scale-0;
}
</style>
