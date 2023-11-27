<template>
  <div class="chat" v-int.show="!isSession && !seen && markMessage">
    <div class="chat-bubble">
      <template v-if="file">
        <component :is="mediaComponent" :file="file" class="my-2 max-h-96" />
      </template>
      <div class="message">
        {{ message.content }}
      </div>
      <div class="h-3 flex gap-0.5 justify-end items-center">
        <span v-if="!isPosted" class="load-anim align-middle p-3 ml-2"></span>
        <template v-else>
          <time class="text-xs opacity-80">{{ createdTime }}</time>
          <span v-if="isSession" class="text-lg align-bottom opacity-80">
            <i v-if="seen" class="bi bi-check2-all"></i>
            <i v-else class="bi bi-check2"></i>
          </span>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import moment from "moment";
import ImgView from "@/components/Media/ImgView.vue";
import VideoView from "@/components/Media/VideoView.vue";
import AudioView from "@/components/Media/AudioView.vue";

export default {
  props: {
    owner: {
      type: Object,
      required: true,
    },
    isSession: {
      type: Boolean,
      required: true,
    },
    message: {
      type: Object,
      required: true,
    },
  },
  computed: {
    file() {
      return this.message.files;
    },

    url() {
      return this.message.url;
    },

    chatCls() {
      return this.isSession ? "chat-end" : "chat-start";
    },

    created() {
      return moment(this.message.created);
    },

    createdTime() {
      return this.created.format("LT");
    },

    isPosted() {
      return this.message.id !== undefined;
    },

    seen() {
      return this.message.seen;
    },

    editPattern() {
      return `message_${this.message.id}_edit`;
    },

    mediaComponent() {
      const { file_type } = this.file;
      if (file_type == "image") return "ImgView";
      if (file_type == "video") return "VideoView";
      if (file_type == "audio") return "AudioView";
    },
  },

  created() {
    this.$session.socket.onChat(this.editPattern, this.messageUpdate);
  },

  unmounted() {
    this.$session.socket.removeChatEvent(this.editPattern, this.messageUpdate);
  },

  methods: {
    async markMessage() {
      await this.$session.patch(this.url, { seen: true });
      const data = {
        event: "edit_message",
        chat_id: this.message.chat,
        message_id: this.message.id,
        data: { seen: true },
      };
      this.$session.socket.send(data);
      this.message.seen = true;
      return true;
    },

    messageUpdate(data) {
      Object.assign(this.message, data);
    },
  },

  components: { ImgView, VideoView, AudioView },
};
</script>

<style scoped>
.chat {
  @apply py-0;
}

.chat-bubble {
  @apply break-words max-w-lg;
}

.load-anim::after {
  @apply loading-spinner text-inherit min-w-[20px];
}
</style>
