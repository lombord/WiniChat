<template>
  <div class="content-div">
    <Sidebar v-model:current="current" />
    <div class="flex-1">
      <ChatDispatcher v-if="current" :current="current" />
      <h2 v-else class="m-auto h-full center-content">
        <span
          class="badge bg-primary-light text-white outline-none border-none text-lg py-4"
        >
          Select a Chat
        </span>
      </h2>
    </div>
    <UserProfile
      v-if="userId && showProfile"
      v-model:show="showProfile"
      :userId="userId"
      :key="userId"
    />
  </div>
</template>

<script>
import Sidebar from "@/components/Sidebar";
import ChatDispatcher from "@/components/ChatDispatcher/ChatDispatcher.vue";
import UserProfile from "@/components/User/UserProfile.vue";

export default {
  computed: {
    userId: {
      get() {
        return this.$profile.current;
      },
      set(val) {
        this.$profile.current = val;
      },
    },

    current: {
      get() {
        return this.$chats.current;
      },
      set(val) {
        this.$chats.current = val;
      },
    },

    showProfile: {
      get() {
        return this.$profile.showProfile;
      },
      set(val) {
        this.$profile.showProfile = val;
      },
    },
  },

  beforeMount() {
    this.$chats.$reset();
  },

  components: { Sidebar, ChatDispatcher, UserProfile },
};
</script>

<style scoped>
.content-div {
  @apply flex h-screen overflow-hidden;
}
</style>
