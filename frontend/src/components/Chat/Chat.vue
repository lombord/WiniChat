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
            class="icon-btn py-2.5 px-3 opacity-60 hover:opacity-100"
          >
            <i
              v-if="!showSide"
              class="bi bi-layout-sidebar-inset-reverse py-0.5"
            ></i>
            <i v-else class="fa-solid fa-xmark"></i>
          </button>
        </div>
      </div>
      <div class="messages-main">
        <Messages
          @vue:mounted="scrollBottom()"
          v-if="dataList.length"
          :messages="dataList"
          :user="user"
          :companion="companion"
        >
          <template #top>
            <div v-int="loadPrevious" class="pt-20">
              <div class="load-anim observer"></div>
            </div>
          </template>
          <template #bottom>
            <div v-int="loadNext" class="pb-32">
              <div class="load-anim observer"></div>
            </div>
          </template>
        </Messages>
      </div>
      <ChatInput :message="message" @submit="postMsg">
        <template v-if="showScroll" #top>
          <div
            class="absolute bottom-20 inset-x-0 pointer-events-none text-center"
          >
            <button
              @click="scrollBottom({ behavior: 'smooth' })"
              class="btn to-bottom"
            >
              <i class="fa-solid fa-chevron-down"></i>
            </button>
          </div>
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
    scrollTop: 0,
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

  mounted() {
    this.scrollTop = this.fetchElm.scrollTop;
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
      this.fetchElm.scrollTo({ top: this.fetchElm.scrollHeight, ...options });
    },

    scrollTo(height) {
      this.fetchElm.scrollTo({ top: height });
    },

    scrolled({ target: el }) {
      this.scrollTop = el.scrollTop;
      this.showScroll = !(
        Math.abs(el.scrollHeight - el.scrollTop - el.clientHeight) < 150
      );
    },
  },

  activated() {
    this.scrollTo(this.scrollTop);
  },

  mixins: [fetchData],
  emits: ["submit"],
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
  @apply btn-primary  py-4
  rounded-full opacity-60
  pointer-events-auto
  hover:opacity-100 btn-square;
}

.chat-top {
  @apply sticky top-0 flex items-center justify-between
  bg-base-200/50 backdrop-blur-3xl px-4 border-b
  z-[10] py-2 shrink-0
  border-base-content/10;
}

.user-short {
  @apply flex gap-2 items-center truncate;
}

.messages-main {
  @apply flex-1 px-4;
}

.observer {
  @apply mt-2 py-3.5;
}

.observer.load-anim::after {
  @apply loading-spinner w-[30px];
}
</style>
