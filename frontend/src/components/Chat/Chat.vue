<template>
  <div ref="fetchElm" class="main-div">
    <div class="messages-main">
      <Messages
        @vue:mounted="scrollBottom"
        @removeMsg="removeMsg"
        @editMsg="editMsg"
        @messageSeen="chat.unread = Math.max(chat.unread - 1, 0)"
        v-if="dataList.length"
        :messages="dataList"
        :user="user"
        :companion="companion"
      >
        <template v-if="previous" #top>
          <div v-int="loadPrevious" class="pt-20">
            <div class="load-anim observer"></div>
          </div>
        </template>
        <template v-if="next" #bottom>
          <div v-int="loadNext" class="pb-32">
            <div class="load-anim observer"></div>
          </div>
        </template>
      </Messages>
    </div>
    <ChatInput
      :editing="editing"
      :message="message"
      @submit="postMsg"
      @cancelEdit="cancelEdit"
      @edited="saveEdit"
    >
      <template v-if="showScroll" #top>
        <div
          class="absolute bottom-20 inset-x-0 pointer-events-none text-center"
        >
          <button
            @click="scrollBottom({ behavior: 'smooth' })"
            class="btn to-bottom"
          >
            <span
              v-if="chat.unread"
              class="absolute -top-2 text-base aspect-square h-6 grid content-center p-1 bg-secondary rounded-full"
            >
              {{ chat.unread }}
            </span>
            <i class="fa-solid fa-chevron-down"></i>
          </button>
        </div>
      </template>
    </ChatInput>
  </div>
</template>

<script>
import fetchData from "@/mixins/fetchData.js";
import Messages from "./Messages.vue";
import ChatInput from "./ChatInput";

export default {
  expose: ['scrolled'],
  data: () => ({
    message: null,
    showScroll: false,
    scrollTop: 0,
    editing: false,
    saveCB: null,
  }),

  props: {
    chat: {
      type: Object,
      required: true,
    },
    scrollElm: {
      type: Element,
      required: true,
    },
  },

  computed: {
    companion() {
      return this.chat.companion;
    },

    user() {
      return this.$session.user;
    },

    url() {
      const { unread } = this.chat;
      return `${this.chat.url}?offset=${unread && unread - 1}`;
    },

    isFullScroll() {
      return (
        this.scrollTop + this.scrollElm.clientHeight >=
        this.scrollElm.scrollHeight
      );
    },

    socket() {
      return this.$session.socket;
    },
  },

  created() {
    this.socket.joinChat(
      this.chat.id,
      this.addMsg,
      this.updateMsg,
      ({ message_id }) => this.removeMsg(message_id)
    );
    this.resetMsg();
  },

  mounted() {
    this.scrollTop = this.scrollElm.scrollTop;
  },

  beforeUnmount() {
    this.socket.leaveChat(this.chat.id);
  },

  methods: {
    async postMsg(tmpFiles) {
      const { content, files } = this.message;
      if (!(content || files.length)) return;
      const data = files.length ? this.toFormData(this.message) : this.message;
      const msg = this.addMsg(this.message, true);
      msg.files = tmpFiles;
      this.resetMsg();
      const prom = this.$session.post(this.url, data);
      try {
        const response = await this.$session.animate(prom, null, "xyz");
        Object.assign(msg, response.data);
        this.$nextTick(this.scrollBottom);
        this.chat.latest = msg;
        this.socket.sendChat(this.chat.id, msg);
      } catch (error) {
        this.$flashes.error("Something went wrong");
      }
    },

    toFormData(msg) {
      const form = new FormData();
      form.append("content", msg.content);
      for (let i = 0; i < msg.files.length; i++)
        form.append("files", msg.files[i]);
      return form;
    },

    resetMsg() {
      this.message = {
        content: "",
        files: [],
      };
    },

    addMsg(msg, scroll = false) {
      if (this.previous) return;
      this.dataList.unshift(msg);
      (scroll || this.isFullScroll) && this.$nextTick(this.scrollBottom);
      return this.dataList[0];
    },

    updateMsg({ message_id, data }) {
      const msg = this.dataList.find(({ id }) => id == message_id);
      msg && Object.assign(msg, data);
    },

    removeMsg(id) {
      const idx = this.dataList.findIndex((msg) => msg.id == id);
      if (idx >= 0) {
        const [msg] = this.dataList.splice(idx, 1);
        if (!msg.seen && msg.owner != this.user.id) {
          this.chat.unread = Math.max(chat.unread - 1, 0);
        }
      }
    },

    async editMsg(msg, saveCB) {
      this.cancelEdit();
      await this.$nextTick();
      this.editing = true;
      this.saveCB = saveCB;
      this.message = { ...msg };
    },

    cancelEdit() {
      this.editing = false;
      this.saveCB = null;
      this.resetMsg();
    },

    saveEdit() {
      const { content } = this.message;
      this.saveCB(content);
      this.cancelEdit();
    },

    scrollBottom(options) {
      this.scrollElm.scrollTo({ top: this.scrollElm.scrollHeight, ...options });
    },

    scrollTo(height) {
      this.scrollElm.scrollTo({ top: height });
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
  components: { ChatInput, Messages },
};
</script>

<style scoped>
.main-div {
  @apply flex flex-col relative flex-1 h-full;
}

.to-bottom {
  @apply btn-primary  py-4
  rounded-full opacity-60
  relative
  pointer-events-auto
  hover:opacity-100 btn-square;
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
