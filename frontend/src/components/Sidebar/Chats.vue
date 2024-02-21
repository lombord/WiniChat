<template>
  <div class="chats">
    <TransitionGroup name="chats">
      <component
        v-if="chats.size"
        :is="getComponent(chat)"
        v-for="chat in sortedChats"
        :key="getKey(chat)"
        :chat="chat"
        :ref="`chat(${getKey(chat)})`"
        @click="$emit('update:current', chat)"
        class="chat-box"
      />
    </TransitionGroup>
  </div>
</template>

<script>
import Chat from "./Chat.vue";
import GroupChat from "./GroupChat.vue";

export default {
  props: {
    chats: {
      type: Map,
      required: true,
    },

    current: {
      type: [Object, null],
      required: true,
    },
  },

  computed: {
    sortedChats() {
      return Array.from(this.chats.values()).sort((ch1, ch2) => {
        const [a, b] = [this.maxDate(ch2), this.maxDate(ch1)];
        return a >= b ? 1 : -1;
      });
    },

    getKey() {
      return this.$chats.getChatKey;
    },
  },

  methods: {
    maxDate({ created, latest }) {
      if (latest) {
        created = latest.created;
      }
      return Date.parse(created);
    },

    getComponent(chat) {
      return chat.type == "chat" ? "Chat" : "GroupChat";
    },
  },

  components: {
    Chat,
    GroupChat,
  },

  watch: {
    current(chat) {
      if (chat) {
        let elm = null;
        try {
          elm = this.$refs[`chat(${this.getKey(chat)})`][0].$el;
        } catch (error) {}
        if (!elm) return;
        this.$el
          .querySelectorAll(".chat-active")
          .forEach((child) => child.classList.remove("chat-active"));
        elm.classList.add("chat-active");
      }
    },
  },
};
</script>

<style scoped>
.chats {
  @apply overflow-y-auto flex flex-col 
  gap-1
  pl-2 pr-1;
}

.chats-move {
  @apply transition duration-300;
}

.chat-box {
  @apply flex gap-2 items-start p-[0.4rem] pr-2.5
  cursor-pointer 
  bg-base-content/5
  rounded-[1.2rem];
}

.chat-box:hover:not(.chat-active) {
  @apply hover:bg-base-content/15;
}

.chat-active {
  @apply bg-primary-light text-white/80;
}

.chat-box:deep(.chat-name) {
  @apply text-base-content flex-1;
}

.chat-active :deep(.chat-name) {
  @apply text-white;
}

.chat-box :deep(.chat-pill) {
  @apply p-1 min-w-[1.5rem] flex items-center 
  justify-center h-6 rounded-full bg-primary-light/80
   text-white;
}

.chat-active :deep(.chat-pill) {
  @apply bg-white text-primary;
}
</style>
