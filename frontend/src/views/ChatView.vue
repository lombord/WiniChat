<template>
  <div class="main-div">
    <Sidebar v-model:current="current" />
    <div class="flex-1">
      <KeepAlive v-if="current" :max="6">
        <component is="Chat" :chat="current" :key="current.id" />
      </KeepAlive>
      <h2 v-else class="m-auto h-full center-content">
        <span class="badge badge-primary text-lg py-4">Select a Chat</span>
      </h2>
    </div>
  </div>
</template>

<script>
import Sidebar from "@/components/Sidebar";
import Chat from "@/components/Chat";

export default {
  data: () => ({
    current: null,
  }),

  components: { Sidebar, Chat },
};
</script>

<style scoped>
.main-div {
  @apply flex h-screen overflow-hidden;
}
</style>
