<template>
  <div class="flex h-full overflow-hidden" v-if="current">
    <div
      @vue:mounted="scrollElm = $refs.scrollElm"
      class="chat-center overflow-x-hidden"
      ref="scrollElm"
    >
      <ChatTop class="z-50" v-model:showSide="showSide" :chat="current" />
      <Chat
        class="flex-1 relative z-[1]"
        :chat="current"
        :scrollElm="scrollElm"
      />
    </div>
    <ChatSide :chat="current" class="chat-side" :show="showSide" />
  </div>
</template>

<script>
import ChatTop from "./ChatTop.vue";
import Chat from "./Chat.vue";
import ChatSide from "./ChatSide.vue";

export default {
  data: () => ({
    showSide: false,
    scrollElm: null,
  }),

  props: {
    current: {
      type: Object,
      required: true,
    },
  },

  computed: {
    companion() {
      return this.current.companion;
    },
  },

  components: { Chat, ChatTop, ChatSide },
};
</script>

<style scoped>
.chat-center {
  @apply flex-1 flex flex-col overflow-y-auto;
  scrollbar-gutter: stable;
}

@supports not selector(::-webkit-scrollbar) {
  .chat-center {
    scrollbar-color: transparent theme("colors.base-200");
  }

  .chat-center:hover {
    scrollbar-color: theme("colors.base-content/20%") theme("colors.base-200");
  }
}

.chat-center::-webkit-scrollbar-track {
  @apply bg-base-200;
}

:deep(.chat-side) {
  @apply flex-[0.5] min-w-[200px] max-w-[450px]
  overflow-y-auto z-50 relative overflow-x-hidden
  bg-base-200;
}
</style>
