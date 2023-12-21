<template>
  <div class="content-div">
    <Sidebar v-model:current="current" />
    <div class="flex-1">
      <div class="flex h-full overflow-hidden" v-if="current">
        <div
          @vue:mounted="scrollElm = $refs.scrollElm"
          @scroll="$refs.messages.scrolled"
          class="chat-center"
          ref="scrollElm"
        >
          <ChatTop
            class="z-50"
            v-model:showSide="showSide"
            :companion="companion"
          />
          <KeepAlive :max="3">
            <component
              class="flex-1"
              is="Chat"
              ref="messages"
              :chat="current"
              :key="current.id"
              v-if="scrollElm"
              :scrollElm="scrollElm"
            />
          </KeepAlive>
        </div>
        <KeepAlive :max="3">
          <ChatSide
            class="chat-side"
            v-if="showSide"
            :key="current.id"
            :user="companion"
            :filesUrl="current.files_url"
          />
        </KeepAlive>
      </div>
      <h2 v-else class="m-auto h-full center-content">
        <span class="badge badge-primary text-lg py-4">Select a Chat</span>
      </h2>
    </div>
  </div>
</template>

<script>
import Sidebar from "@/components/Sidebar";
import Chat from "@/components/Chat";
import ChatTop from "@/components/Chat/ChatTop.vue";
import ChatSide from "@/components/Chat/ChatSide";

export default {
  data: () => ({
    current: null,
    showSide: false,
    scrollElm: null,
  }),

  computed: {
    companion() {
      return this.current.companion;
    },
  },

  components: { Sidebar, Chat, ChatTop, ChatSide },
};
</script>

<style scoped>
.content-div {
  @apply flex h-screen overflow-hidden;
}

.chat-center {
  @apply flex-1 flex flex-col overflow-y-auto;
}
.chat-center::-webkit-scrollbar-track {
  @apply bg-base-200;
}

.chat-side {
  @apply flex-[0.45] min-w-[200px] max-w-[500px];
}
</style>
