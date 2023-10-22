<template>
  <div class="chats">
    <TransitionGroup name="chats">
      <Chat
        v-bind="$attrs"
        v-for="chat in sortedChats"
        :key="chat.id"
        :chat="chat"
      />
    </TransitionGroup>
    <slot name="bottom"></slot>
  </div>
</template>

<script>
import Chat from "./Chat.vue";
export default {
  props: {
    chats: {
      type: Array,
      default: () => [],
    },
  },
  computed: {
    sortedChats() {
      return this.chats.toSorted((ch1, ch2) => {
        const [a, b] = [this.maxDate(ch2), this.maxDate(ch1)];
        return a >= b ? 1 : -1;
      });
    },
  },

  methods: {
    maxDate({ created, latest }) {
      if (latest) {
        created = latest.created;
      }
      return Date.parse(created);
    },
  },
  components: { Chat },
  inheritAttrs: false,
};
</script>

<style scoped>
.chats {
  @apply overflow-y-auto flex flex-col gap-2 pr-1;
}

.chats-move {
  @apply transition duration-300;
}
</style>
