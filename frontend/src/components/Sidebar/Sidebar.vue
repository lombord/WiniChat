<template>
  <div class="side-root pop-btn-parent">
    <div class="m-sidebar flex flex-col">
      <SideTop :chats="chats" />
      <FetchObserver
        class="chats-box"
        ref="fetchElm"
        :hasBottom="!!next"
        :fetchBottom="fetchNext"
      >
        <Chats v-if="chats.size" :chats="chats" v-model:current="currChat" />
        <h3 v-else class="text-primary text-center">Empty</h3>
      </FetchObserver>
    </div>
    <div class="side-resize" @mousedown.left.capture="mouseDown = true"></div>
    <div class="pop-btn-box">
      <button @click="showCG = true" class="pop-btn">
        <i class="fa-solid fa-user-group"></i>
      </button>
    </div>
    <CreateGroup v-if="showCG" v-model:show="showCG" />
  </div>
</template>

<script>
import fetchData from "@/mixins/fetchData.js";
import CreateGroup from "@/components/Group/CreateGroup.vue";

import Chats from "./Chats.vue";
import SideTop from "./SideTop.vue";

export default {
  data: () => ({
    mouseDown: false,
    width: 370,
    showCG: false,
    fetchUrl: "all-chats/",
  }),

  props: {
    current: {
      type: [Object, null],
      required: true,
    },
  },

  computed: {
    user() {
      return this.$session.user;
    },

    socket() {
      return this.$session.socket;
    },

    chats: {
      get() {
        return this.$chats.chatsMap;
      },
      set(val) {
        this.$chats.chatsMap = val;
      },
    },

    currChat: {
      get() {
        return this.current;
      },
      set(val) {
        this.$emit("update:current", val);
      },
    },
  },

  created() {
    const { socket } = this;
    socket.onUser("new_msg", this.newMessage);

    socket.onUser("new_chat", ({ type, chat_id }) => {
      if (!this.$chats.has(type, chat_id)) {
        this.fetchChat(type, chat_id);
      }
    });
    socket.onUser("remove_chat", ({ type, chat_id }) =>
      this.$chats.remove(type, chat_id)
    );
    socket.onUser("group_update", ({ group_id, data }) => {
      const group = this.$chats.get("group", group_id);
      if (group) Object.assign(group, data);
    });
  },

  mounted() {
    this.setListeners();
  },

  beforeUnmount() {
    const { socket } = this;
    try {
      socket.removeUserEvent("new_msg");
      socket.removeUserEvent("new_chat");
      socket.removeUserEvent("remove_chat");
      socket.removeUserEvent("group_update");
    } catch (error) {}
    this.removeListeners();
  },

  methods: {
    firstAdd(data) {
      this.chats = new Map();
      this.addNext(data);
    },

    addNext(data) {
      for (const chat of data) {
        this.$chats.add(chat);
      }
    },

    newMessage({ type, chat_id, data }) {
      const chat = this.$chats.get(type, chat_id);
      if (chat) {
        chat.latest = data;
        data.owner !== this.user.id && chat.unread++;
      } else this.fetchChat(type, chat_id);
    },

    async fetchChat(type, chat_id) {
      let url = `chats/${chat_id}/`;
      if (type == "group") {
        url = `groups/${chat_id}/`;
      }
      const { data } = await this.$session.get(url);
      this.$chats.add(data);
    },

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
  },

  components: { Chats, SideTop, CreateGroup },
  mixins: [fetchData],
};
</script>

<style scoped>
.side-root {
  @apply flex relative z-[100];
  --width: calc(v-bind(width) * 1px);
  width: clamp(max(100px, 10%), 35%, min(var(--width), 35%));
}

.side-resize {
  @apply px-1 cursor-ew-resize absolute 
  inset-y-0 -right-2;
}

.m-sidebar {
  @apply py-4 md:py-4
  h-screen w-full
  border-r border-base-content/10
  overflow-y-auto bg-base-200;
}

.m-sidebar {
  @apply pb-0;
}

.chats-box {
  @apply flex-1 shrink-0 overflow-y-auto;
}

.chats-box.load-anim::after {
  @apply loading-ring;
}
</style>
