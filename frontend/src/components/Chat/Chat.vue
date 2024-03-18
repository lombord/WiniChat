<template>
  <div ref="fetchElm" class="main-div">
    <FetchObserver
      class="messages-main"
      v-if="loaded"
      :hasTop="!!next"
      :fetchTop="fetchNext"
      :hasBottom="!!previous"
      :fetchBottom="fetchPrevious"
    >
      <Messages
        @vue:mounted="scrollBottom()"
        :messages="messages"
        :getContextMenu="getContextMenu"
        @msgSeen="markMessage"
      />
    </FetchObserver>

    <ScrollBottom
      :show="showScroll"
      :unread="chat.unread"
      @scrolled="scrollBottom({ behavior: 'smooth' })"
    />

    <ChatInput
      :editing="!!editing"
      :message="message"
      @submit="postMsg"
      @cancelEdit="cancelEdit"
      @edited="saveEdit"
    />
  </div>
</template>

<script>
// mixins
import chatMixin from "@/components/ChatCommon/chatMixin";

export default {
  expose: ["scrolled"],

  computed: {
    companion() {
      return this.chat.companion;
    },

    fetchUrl() {
      const { unread = 0 } = this.chat;
      return `${this.url}messages/?offset=${unread && unread - 1}`;
    },
  },

  created() {
    this.socket.connectChat(
      this.chat.id,
      this.addMsg,
      this.updateMsg,
      ({ msg_id }) => this.removeMsg(msg_id)
    );
  },

  beforeUnmount() {
    this.socket.disconnectChat(this.chat.id);
  },

  methods: {
    messagePosted(data) {
      this.socket.sendChatMsg(this.chat.id, data);
    },

    msgPatched(msg, data, rData) {
      this.socket.sendChatEvent({
        event: "edit_msg",
        chat_id: this.chat.id,
        msg_id: msg.id,
        data,
      });
    },

    msgDeleted(msg) {
      this.socket.sendChatEvent({
        event: "del_msg",
        chat_id: this.chat.id,
        msg_id: msg.id,
      });
    },

    async markMessage(msg) {
      await this.patchMessage(msg, { seen: true });
      this.message.seen = true;
      this.chat.unread = Math.max(this.chat.unread - 1, 0);
    },

    // markAllAbove(idx) {
    //   for (let i = idx; i < this.dataList.length; i++) {
    //     const msg = this.dataList[i];
    //     if (msg.seen || msg.owner != this.user.id) return;
    //     msg.seen = true;
    //   }
    // },
  },

  mixins: [chatMixin],
};
</script>

<style scoped>
.main-div {
  @apply flex flex-col relative flex-1 h-full;
}

.messages-main {
  @apply flex-1 px-3;
}

.observer {
  @apply mt-2 py-3.5;
}


</style>
