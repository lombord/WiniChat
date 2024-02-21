<template>
  <div class="chat-box">
    <UserAvatar :user="companion" />
    <div class="flex-1 truncate">
      <div class="flex gap-1 items-center">
        <h6 class="chat-name">
          {{ companion.full_name }}
        </h6>
        <p v-if="latest" class="text-sm">
          {{ created }}
        </p>
      </div>
      <div v-if="latest" class="flex items-center gap-1">
        <p class="truncate flex-1">
          {{ latest.content }}
        </p>
        <div v-if="isSession || unread" class="chat-pill">
          <span v-if="isSession">
            <i v-if="latest.seen" class="bi bi-check2-all"></i>
            <i v-else class="bi bi-check2"></i>
          </span>
          <span v-else>
            {{ unread }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import chatMixin from "./chatMixin";
import UserAvatar from "@/components/User/UserAvatar.vue";
import trackUser from "@/components/User/trackUser.js";

export default {
  computed: {
    companion: {
      get() {
        return this.chat.companion;
      },
      set(value) {
        this.chat.companion = value;
      },
    },

    user() {
      return this.companion;
    },

    userId() {
      return this.companion.id;
    },

    socket() {
      return this.$session.socket;
    },
  },

  created() {
    this.socket.refreshUser(this.companion);
  },

  mixins: [chatMixin, trackUser],
  components: { UserAvatar },
};
</script>

<style scoped></style>
