<template>
  <aside class="side-root" :style="{ '--width': `${width}px` }">
    <div class="m-sidebar flex flex-col">
      <SideUser />
      <div class="my-4">
        <button class="find-btn tflex" @click="findShow = true">
          <span class="text-secondary text-xl">
            <i class="fa-solid fa-circle-nodes"></i>
          </span>
          Find People
        </button>
        <FindChat v-if="findShow" :chats="chats" v-model:show="findShow" />
      </div>

      <div
        class="chats-box flex-1 shrink-0 overflow-y-auto pb-2"
        ref="fetchElm"
      >
        <Chats v-if="chats.length" v-bind="$attrs" :chats="chats">
          <template #bottom>
            <div v-int="loadNext" class="pt-10">
              <div class="observer load-anim"></div>
            </div>
          </template>
        </Chats>
        <h3 v-else class="text-primary text-center">Empty</h3>
      </div>
    </div>
    <div class="side-resize" @mousedown.left.capture="mouseDown = true"></div>
  </aside>
</template>

<script>
import fetchData from "@/mixins/fetchData.js";

import SideUser from "./SideUser.vue";
import FindChat from "@/components/FindChat";
import Chats from "./Chats.vue";

export default {
  data: () => ({
    mouseDown: false,
    findShow: false,
    width: 400,
    url: "chats/",
  }),

  computed: {
    user() {
      return this.$session.user;
    },
    socket() {
      return this.$session.socket;
    },
    chats() {
      return this.dataList;
    },
  },

  created() {
    this.socket.onChat("last_message", this.newMessage);
    this.socket.onChat("new_chat", ({ chat_id }) => this.fetchChat(chat_id));
  },

  mounted() {
    this.setListeners();
  },

  beforeUnmount() {
    try {
      this.socket.removeChatCB("last_message", this.newMessage);
    } catch (error) {}
    this.removeListeners();
  },

  methods: {
    setListeners() {
      this.resize = ({ x }) => {
        if (!this.mouseDown) return;
        this.width = x;
      };
      this.stop = () => (this.mouseDown = false);
      this.$root.$el.addEventListener("mousemove", this.resize);
      window.addEventListener("mouseup", this.stop);
      window.addEventListener("mouseleave", this.stop);
    },

    removeListeners() {
      this.$root.$el.removeEventListener("mousemove", this.resize);
      window.removeEventListener("mouseup", this.stop);
      window.removeEventListener("mouseleave", this.stop);
    },

    newMessage(data) {
      const { chat: chatId } = data;
      const chat = this.chats.find(({ id }) => id === chatId);
      if (chat) {
        chat.latest = data;
        chat.latest.owner !== this.user.id && chat.unread++;
      } else this.fetchChat(chatId);
    },

    async fetchChat(chatId) {
      const {
        data: { results },
      } = await this.$session.get(`chats?id=${chatId}`);
      this.chats.push(results[0]);
    },
  },

  components: { SideUser, FindChat, Chats },
  mixins: [fetchData],
};
</script>

<style scoped>
.side-root {
  @apply flex relative z-[100];
  --width: 200px;
  width: clamp(max(100px, 10%), 35%, min(var(--width), 35%));
}

.side-resize {
  @apply px-1 cursor-ew-resize absolute 
  inset-y-0 -right-2;
}

.m-sidebar {
  @apply p-4 px-3 md:p-6
  h-screen w-full
  border-r border-base-content/10
  overflow-y-auto bg-base-200;
}

.m-sidebar {
  @apply pb-0;
}

.find-btn {
  @apply btn py-2.5 break-words btn-primary 
  w-full block min-h-fit h-auto;
}

.chats-box.load-anim::after {
  @apply loading-ring;
}

.observer {
  @apply py-3.5 my-2;
}
.observer.load-anim::after {
  @apply loading-spinner w-[8%];
}
</style>
