<template>
  <div class="main-div">
    <div
      class="flex gap-2 items-center truncate bg-base-200 px-4 py-2 border-b border-base-content/20"
    >
      <div class="avatar" :class="avatarCls">
        <div class="round-img w-16">
          <img :src="companion.photo" />
        </div>
      </div>
      <h5 class="text-primary">{{ username }}</h5>
    </div>
    <div ref="fetchElm" class="messages-main">
      <Messages
        @vue:mounted="scrollBottom"
        v-if="dataList.length"
        :messages="dataList"
        :user="user"
        :companion="companion"
      >
        <template #bottom>
          <div v-int="intersected" class="load-anim observer"></div>
        </template>
      </Messages>
    </div>
    <ChatInput v-model="content" @submit.prevent="postMsg" />
  </div>
</template>

<script>
import fetchData from "@/mixins/fetchData.js";

import Messages from "./Messages.vue";
import ChatInput from "./ChatInput.vue";

export default {
  data: () => ({
    config: { baseURL: "" },
    content: "",
  }),

  props: {
    chat: {
      type: Object,
      required: true,
    },
  },

  computed: {
    companion() {
      return this.chat.companion;
    },

    username() {
      return this.companion.full_name || this.companion.username;
    },

    user() {
      return this.$session.user;
    },

    url() {
      return this.chat.url;
    },
    avatarCls() {
      return this.companion.status ? "online" : "offline";
    },
    socket() {
      return this.$session.socket;
    },
  },

  created() {
    this.socket.joinChat(this.chat.id, this.addMsg);
  },

  beforeUnmount() {
    this.socket.leaveChat(this.chat.id, this.addMsg);
  },

  methods: {
    async postMsg() {
      if (!this.content) return;
      const data = { content: this.content };
      this.content = "";
      const msg = this.addMsg(data);
      const prom = this.$session.post(this.url, data);
      const response = await this.$session.animate(prom, null, "xyz");
      Object.assign(msg, response.data);
      this.chat.latest = msg;
      this.socket.sendChat(this.chat.id, msg);
    },

    addMsg(msg) {
      this.dataList.unshift(msg);
      this.scrollBottom();
      return this.dataList[0];
    },

    scrollBottom() {
      const el = this.$refs.fetchElm;
      el.scrollTo(0, el.scrollHeight);
    },
  },

  activated() {
    this.scrollBottom();
  },

  mixins: [fetchData],
  components: { ChatInput, Messages },
};
</script>

<style scoped>
.main-div {
  @apply flex flex-col;
}

.messages-main {
  @apply flex-1 overflow-y-auto px-4 sm:px-5 md:px-6 xl:px-8;
}

.observer {
  @apply mt-2 py-3.5;
}

.observer.load-anim::after {
  @apply loading-spinner w-[30px];
}
</style>
