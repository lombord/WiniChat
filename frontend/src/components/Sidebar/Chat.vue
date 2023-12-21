<template>
  <div
    class="chat-box"
    :class="{ 'chat-active': isActive }"
    @click="$emit('update:current', chat)"
  >
    <div class="avatar" :class="avatarCls">
      <div class="round-img w-16">
        <img :src="companion.photo" />
      </div>
    </div>
    <div class="flex-1 truncate">
      <div class="flex gap-1 items-center">
        <h6 class="text-primary flex-1">
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
        <div
          v-if="isSession || unread"
          class="text-md p-1 min-w-[1.5rem] flex items-center justify-center
          h-6 
          rounded-full bg-primary/30 text-white"
        >
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
import moment from "moment";

export default {
  props: {
    chat: {
      type: Object,
      required: true,
    },
    current: {
      required: true,
    },
  },

  computed: {
    companion: {
      get() {
        return this.chat.companion;
      },
      set(value) {
        this.chat.companion = value;
      },
    },

    latest() {
      return this.chat.latest;
    },

    isSession() {
      return this.latest.owner == this.$session.user.id;
    },

    unread() {
      return this.chat.unread;
    },

    created() {
      const data = moment(this.latest.created);
      return data.calendar(null, {
        sameDay: "LT",
        nextWeek: "ddd",
        lastDay: "[Yester.]",
        lastWeek: "ddd",
        sameElse: "DD/MM/YYYY",
      });
    },

    isActive() {
      if (!this.current) return;
      return this.chat.id === this.current.id;
    },

    avatarCls() {
      return this.companion.status ? "online" : "offline";
    },

    socket() {
      return this.$session.socket;
    },
  },

  created() {
    const { id } = this.companion;
    this.socket.watchUser(id, this.userJoint, this.userLeft);
    this.socket.onUser(`${id}_edit`, this.userEdit);
  },

  beforeUnmount() {
    const { id } = this.companion;
    this.socket.leaveUser(id, this.userJoint, this.userLeft);
    this.socket.removeUserEvent(`${id}_edit`, this.userEdit);
  },

  methods: {
    userJoint() {
      this.companion.status = 1;
    },
    userLeft() {
      this.companion.status = 0;
    },
    userEdit(data) {
      Object.assign(this.companion, data);
    },
  },
};
</script>

<style scoped>
.chat-box {
  @apply flex gap-2 items-start p-1.5 px-2 
  cursor-pointer
  bg-base-300/80
  focus:bg-secondary/10
  hover:bg-primary/10 rounded-xl;
}

.chat-active {
  @apply bg-primary/10;
}
</style>
