<template>
  <div>
    <div class="round-img w-16 overflow-hidden">
      <ImgAnim :src="chat.photo" class="full-img" />
    </div>
    <div class="flex-1 truncate">
      <div class="flex gap-1 items-center">
        <div class="flex-1 icon-flex">
          <span class="group-icon">
            <i v-if="chat.public" class="fa-solid fa-users text-base"></i>
            <i v-else class="fa-solid fa-user-group"></i>
          </span>
          <h6 class="chat-name flex-1 w-0">
            {{ chat.name }}
          </h6>
        </div>
        <p v-if="latest" class="text-sm">
          {{ created }}
        </p>
      </div>
      <div v-if="latest" class="icon-flex">
        <div class="flex-1 flex gap-1 truncate">
          <div class="msg-owner">{{ owner_name }}:</div>
          <p class="flex-1">{{ latest.content }}</p>
        </div>
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

export default {
  props: {
    chat: {
      type: Object,
      required: true,
    },
  },

  computed: {
    owner_name() {
      return this.isSession ? "You" : this.latest.owner_name;
    },
  },

  mixins: [chatMixin],
};
</script>

<style scoped>
.group-icon {
  @apply text-xs text-secondary;
}
.chat-active .group-icon {
  @apply text-[inherit];
}

.msg-owner {
  @apply text-accent/80 truncate max-w-[200px];
}

.chat-active .msg-owner {
  @apply text-white;
}

.chat-active .group-icon {
  @apply text-white;
}
</style>
