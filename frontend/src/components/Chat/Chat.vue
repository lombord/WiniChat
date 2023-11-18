<template>
  <div class="root-div">
    <div @scroll="scrolled" ref="fetchElm" class="main-div">
      <div class="chat-top">
        <div class="user-short">
          <div class="avatar" :class="avatarCls">
            <div class="round-img w-16">
              <img :src="companion.photo" />
            </div>
          </div>
          <h5 class="text-primary">{{ username }}</h5>
        </div>
        <div class="">
          <button
            @click="showSide = !showSide"
            class="btn p-0 btn-ghost rounded-full text-lg opacity-60 hover:opacity-100"
          >
            <i
              v-if="!showSide"
              class="bi bi-layout-sidebar-inset-reverse py-2 px-3.5"
            ></i>
            <i v-else class="fa-solid py-2.5 px-3 fa-xmark"></i>
          </button>
        </div>
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
      <ChatInput :message="message" @submit="postMsg">
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

    <ChatSide :user="companion" :show="showSide" />
  </div>
</template>

<script>
import fetchData from "@/mixins/fetchData.js";

import Messages from "./Messages.vue";
import ChatInput from "./ChatInput.vue";
import ChatSide from "./ChatSide.vue";

export default {
  data: () => ({
    message: null,
    showScroll: false,
    showSide: false,
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
    this.resetMsg();
  },

  beforeUnmount() {
    this.socket.leaveChat(this.chat.id, this.addMsg);
  },

  methods: {
    async postMsg(tmpFile, resetCB) {
      if (!(this.message.content || this.message.file)) return;
      const data = this.message.file
        ? this.toFormData(this.message)
        : this.message;
      const msg = this.addMsg(this.message);
      msg.files = tmpFile;
      this.resetMsg();
      resetCB();
      const prom = this.$session.post(this.url, data);
      try {
        const response = await this.$session.animate(prom, null, "xyz");
        Object.assign(msg, response.data);
        this.$nextTick(this.scrollBottom);
        this.chat.latest = msg;
        this.socket.sendChat(this.chat.id, msg);
      } catch (error) {
        this.$flashes.error("Invalid file type!");
      }
    },

    toFormData(obj) {
      const form = new FormData();
      for (const key in obj) {
        form.append(key, obj[key]);
      }
      return form;
    },

    resetMsg() {
      this.message = {
        content: "",
        file: null,
      };
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
  emits: ["submit",],
  components: { ChatInput, Messages, ChatSide },
};
</script>

<style scoped>
.root-div {
  @apply flex h-full overflow-hidden;
}

.main-div {
  @apply flex flex-col relative flex-1
  overflow-y-auto h-full;
}

.main-div::-webkit-scrollbar-track {
  @apply bg-base-200;
}

.to-bottom {
  @apply btn-primary absolute py-4
  rounded-full 
  opacity-60 hover:opacity-100
  bottom-20 right-2 btn-square;
}

.chat-top {
  @apply sticky top-0 flex items-center justify-between
  bg-base-200/50 backdrop-blur-3xl px-4 border-b
  z-[100] py-2 shrink-0
  border-base-content/10;
}

.user-short {
  @apply flex gap-2 items-center truncate;
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
