<template>
  <div class="content-div">
    <Sidebar v-model:current="current" />
    <div class="flex-1">
      <div class="flex h-full overflow-hidden" v-if="current">
        <KeepAlive :max="3">
          <component
            class="flex-1"
            is="Chat"
            v-model:showSide="showSide"
            :chat="current"
            :key="current.id"
          />
        </KeepAlive>
        <ChatSide :user="current.companion" :show="showSide" />
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
import ChatSide from "@/components/Chat/ChatSide.vue";

export default {
  data: () => ({
    current: null,
    showSide: false,
  }),

  components: { Sidebar, Chat, ChatSide },
};
</script>

<style scoped>
.content-div {
  @apply flex h-screen overflow-hidden;
}
</style>
