<template>
  <div @scroll="scrolled" ref="fetchElm" class="main-div">
    <div class="chat-top">
      <div class="avatar" :class="avatarCls">
        <div class="round-img w-16">
          <img :src="companion.photo" />
        </div>
      </div>
      <h5 class="text-primary">{{ username }}</h5>
    </div>
    <div class="messages-main">
      <Messages
        @vue:mounted="scrollBottom"
        v-if="dataList.length"
        :messages="dataList"
        :user="user"
        :companion="companion"
      >
        <template #bottom>
          <div v-int="intersected" class="pb-32">
            <div class="load-anim observer"></div>
          </div>
        </template>
      </Messages>
    </div>

    <ChatInput v-model="content" @submit.prevent="postMsg">
      <template v-if="showScroll" #top>
        <button
          @click="scrollBottom({ behavior: 'smooth' })"
          class="btn to-bottom"
        >
          <i class="fa-solid fa-arrow-down"></i>
        </button>
      </template>
    </ChatInput>
  </div>
</template>

<script>
import fetchData from "@/mixins/fetchData.js";

import Messages from "./Messages.vue";
import ChatInput from "./ChatInput.vue";

export default {
  data: () => ({
    content: "",
    showScroll: false,
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
      this.$nextTick(this.scrollBottom);
      this.chat.latest = msg;
      this.socket.sendChat(this.chat.id, msg);
    },

    addMsg(msg) {
      this.dataList.unshift(msg);
      this.$nextTick(this.scrollBottom);
      return this.dataList[0];
    },

    scrollBottom(options) {
      const el = this.$refs.fetchElm;
      el.scrollTo({ top: el.scrollHeight, ...options });
    },

    scrolled({ target: el }) {
      this.showScroll = !(
        Math.abs(el.scrollHeight - el.scrollTop - el.clientHeight) < 150
      );
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
  @apply flex flex-col relative 
  overflow-y-auto h-full;
}

.to-bottom {
  @apply btn-primary absolute py-4
  rounded-full 
  opacity-60 hover:opacity-100
  bottom-20 right-2 btn-square;
}

.chat-top {
  @apply flex gap-2 items-center truncate sticky top-0
  bg-base-200/50 backdrop-blur-3xl px-4 border-b
  z-10 py-1.5 shrink-0
  border-base-content/10;
}

.messages-main {
  @apply flex-1 px-4 sm:px-5 
  md:px-6 xl:px-8;
}

.observer {
  @apply mt-2 py-3.5;
}

.observer.load-anim::after {
  @apply loading-spinner w-[30px];
}
</style>
