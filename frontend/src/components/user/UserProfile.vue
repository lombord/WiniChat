<template>
  <Modal class="p-0 bg-transparent" v-model:show="mShow">
    <div v-if="loaded">
      <div class="top-box gap-3" :style="{ '--bgUrl': `url(${user.photo})` }">
        <div class="avatar-box">
          <UserAvatar :user="user" class="w-28" />
          <div class="flex-1">
            <h4 class="text-white/90">{{ user.full_name }}</h4>
            <IdTag class="text-white/70">
              {{ user.username }}
            </IdTag>
          </div>
          <div v-if="!isSession">
            <button
              ref="actionBtn"
              @click="(hasChat ? fetchChat : postChat)()"
              class="icon-btn action-btn spinner-on-load"
            >
              <i v-if="hasChat" class="fa-regular fa-pen-to-square"></i>
              <i v-else class="fa-solid fa-user-plus"></i>
            </button>
          </div>
        </div>
      </div>
      <div class="profile-content">
        <CollapseInfo title="Bio">
          {{ user.bio || "Empty" }}
        </CollapseInfo>
      </div>
    </div>
    <div v-else class="min-h-[200px] load-anim bg-base-300"></div>
  </Modal>
</template>

<script>
import trackUser from "./trackUser.js";

import Modal from "@/components/UI/Modal.vue";
import CollapseInfo from "@/components/UI/CollapseInfo.vue";
import startChat from "@/components/Chat/startChat.js";
import UserAvatar from "./UserAvatar.vue";

export default {
  data: () => ({
    user: {},
    loaded: false,
  }),

  props: {
    userId: {
      required: true,
    },
    show: {
      required: true,
      type: Boolean,
    },
  },

  computed: {
    isSession() {
      return this.$session.user.id == this.userId;
    },

    mShow: {
      get() {
        return this.show;
      },

      set(val) {
        this.$emit("update:show", val);
      },
    },

    chatId: {
      get() {
        return this.user.chat_id;
      },
      set(val) {
        this.user.chat_id = val;
      },
    },

    hasChat() {
      return !!this.chatId;
    },
  },

  methods: {
    async postChat() {
      try {
        const prom = this.startChat(this.userId);
        const { data } = await this.$session.animate(
          prom,
          this.$refs.actionBtn
        );
        this.chatId = data.id;
      } catch (err) {
        this.$flasher.axiosError(err);
      }
    },

    async fetchChat() {
      let chat = this.$chats.get("chat", this.chatId);
      if (!chat) {
        const prom = this.$session.get(`chats/${this.chatId}/`);
        ({ data: chat } = await this.$session.animate(
          prom,
          this.$refs.actionBtn
        ));
        this.$chats.add(chat);
      }
      await this.$nextTick();
      this.$chats.current = chat;
      this.$emit("update:show", false);
    },
  },

  async mounted() {
    this.user = await this.$session.fetchUser(this.userId);
    this.loaded = true;
  },

  components: { Modal, UserAvatar, CollapseInfo },
  mixins: [trackUser, startChat],
  emits: ["changeCurrent", "update:show"],
};
</script>

<style scoped>
.top-box {
  @apply blur-0 backdrop-blur-0 z-10
  items-center relative;
}

.top-box::before {
  @apply content-[''] -z-10
  absolute -inset-10 -inset-y-8 blur-xl
  bg-no-repeat bg-cover bg-center bg-base-200;
  background-image: var(--bgUrl);
  transform: translate3d(0, 0, 0);
  backface-visibility: hidden;
}

.top-box::after {
  @apply content-[''] absolute inset-0 -z-10 bg-black/25;
}

.avatar-box {
  @apply flex items-center gap-3 p-4 pt-10;
}

.profile-content {
  @apply p-4 pt-8 bg-base-200;
}

.action-btn {
  @apply text-white/70 text-3xl;
}
</style>
