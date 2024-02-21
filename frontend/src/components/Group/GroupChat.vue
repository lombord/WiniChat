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
        @vue:mounted="scrollBottom"
        :messages="messages"
        :getContextMenu="getContextMenu"
        @msgSeen="1"
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
      :canSend="canSend"
      :canSendLoading="!userRole"
    />
  </div>
</template>

<script>
import { computed } from "vue";

import chatMixin from "@/components/ChatCommon/chatMixin.js";

import permission from "./GroupRoles/permission.js";
import trackMember from "./GroupMembers/trackMember.js";

export default {
  data: () => ({
    autoSetUp: false,
  }),

  computed: {
    group() {
      return this.chat;
    },

    userId() {
      return this.$session.user.id;
    },

    userRole: {
      get() {
        return this.group.user_role;
      },
      set(val) {
        this.group.user_role = val;
      },
    },

    role() {
      return this.userRole;
    },
  },

  async created() {
    this.socket.connectGroup(
      this.groupId,
      (msg) => this.addMsg(msg),
      (msg) => this.updateMsg(msg),
      ({ msg_id }) => this.removeMsg(msg_id)
    );
    this.onGroup("new_members", ({ length }) => this.updateMembers(length));
    this.onGroup("remove_members", ({ length }) => this.updateMembers(-length));
    this.userRole = null;
    const { data } = await this.$session.get(`${this.group.url}my-role/`);
    data.fetched = true;
    this.userRole = data;
    this.setUpWSMember();
    this.refreshWSRole(data);
  },

  beforeUnmount() {
    this.socket.disconnectGroup(this.groupId);
  },

  methods: {
    getContextFor(user) {
      const delOP = this.commonContext.delete;
      const copyOP = this.commonContext.copy;
      return computed(() => [copyOP, { ...delOP, hidden: !this.canDelete }]);
    },

    onGroup(event, callback) {
      this.socket.onGroup(this.groupId, event, callback);
    },

    sendGroup({ event, ...options }) {
      this.socket.sendGroupEvent({
        event,
        group_id: this.groupId,
        ...options,
      });
    },

    messagePosted(data) {
      this.sendGroup({ event: "send", data });
    },

    msgPatched(msg, data, rData) {
      this.sendGroup({ event: "edit_msg", msg_id: msg.id, data });
    },

    msgDeleted(msg) {
      this.sendGroup({ event: "del_msg", msg_id: msg.id });
    },

    updateMembers(count) {
      this.group.members += count;
    },
  },

  mixins: [chatMixin, permission, trackMember],
};
</script>

<style scoped>
.main-div {
  @apply flex flex-col 
  relative flex-1 h-full;
}

.messages-main {
  @apply flex-1 px-3;
}

</style>
