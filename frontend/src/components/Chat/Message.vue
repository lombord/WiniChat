<template>
  <div
    @contextmenu.capture.prevent.stop="toggleContext"
    class="msg-root"
    ref="rootElm"
    :class="{ 'chat-context': show }"
    v-int.show="!isSession && !seen && markMessage"
  >
    <div class="chat" :class="$attrs.class">
      <div class="chat-bubble">
        <template v-if="files.length">
          <div class="files-wrapper">
            <component :is="mediaComponent" :files="files" />
          </div>
        </template>
        <div class="message">
          {{ message.content }}
        </div>
        <div
          class="h-3 flex opacity-80 text-xs gap-0.5 justify-end items-center"
        >
          <span
            v-if="!isPosted || saving"
            class="load-anim align-middle p-3 ml-2"
          ></span>
          <template v-else>
            <span v-if="isEdited" class="mr-1">edited</span>
            <time>{{ createdTime }}</time>
            <span v-if="isSession" class="text-lg align-bottom">
              <i v-if="seen" class="bi bi-check2-all"></i>
              <i v-else class="bi bi-check2"></i>
            </span>
          </template>
        </div>
      </div>
    </div>
    <ContextMenu
      class="message-context"
      ref="contextMenu"
      :style="{ top: `${oY}px`, left: `${oX}px` }"
      v-model:show="show"
      :menu="menu"
    />
  </div>
</template>

<script>
import { defineAsyncComponent } from "vue";
import moment from "moment";

import ContextMenu from "@/components/UI/ContextMenu.vue";

export default {
  data: () => ({
    saving: false,
    show: false,
    oX: 0,
    oY: 0,
  }),

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
    menu() {
      if (this.isSession) {
        return [
          { label: "Copy", cb: this.copyMsg },
          { label: "Edit", cb: this.edit },
          { label: "Delete", cb: this.delete },
        ];
      }
      return [{ label: "Copy", cb: this.copyMsg }];
    },

    files() {
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

    isEdited() {
      return this.message.is_edited;
    },

    mediaComponent() {
      const { file_type } = this.files[0];
      if (file_type == "image") return "ImagesSlide";
      if (file_type == "video") return "VideosSlide";
      if (file_type == "audio") return "AudiosList";
    },

    socket() {
      return this.$session.socket;
    },
  },

  methods: {
    async patchData(data) {
      const { data: rData } = await this.$session.patch(this.url, data);
      this.socket.send({
        event: "edit_message",
        chat_id: this.message.chat,
        message_id: this.message.id,
        data: rData,
      });
      return rData;
    },

    async markMessage() {
      await this.patchData({ seen: true });
      this.message.seen = true;
      this.$emit("messageSeen");
      return true;
    },

    messageUpdate(data) {
      Object.assign(this.message, data);
    },

    async saveChanges(content) {
      this.saving = true;
      this.message.content = content;
      const data = await this.patchData({ content });
      this.messageUpdate(data);
      this.saving = false;
    },

    edit() {
      this.$emit("editMsg", this.message, this.saveChanges);
    },

    async delete() {
      await this.$session.delete(this.url);
      const data = {
        event: "delete_message",
        chat_id: this.message.chat,
        message_id: this.message.id,
      };
      this.socket.send(data);
      this.removeEmit();
    },

    removeEmit() {
      this.$emit("removeMsg", this.message.id);
    },

    async copyMsg() {
      await navigator.clipboard.writeText(this.message.content);
    },

    async toggleContext(e) {
      this.show = !this.show;
      if (!this.show) return;
      await this.$nextTick();
      const rect = this.$refs["contextMenu"].$el.getBoundingClientRect();
      const bRect = document.body.getBoundingClientRect();
      let { clientX, clientY } = e;
      if (clientX + rect.width > bRect.width) {
        clientX = bRect.width - rect.width - 10;
      }
      if (clientY + rect.height > bRect.height) {
        clientY = bRect.height - rect.height - 10;
      }
      [this.oX, this.oY] = [clientX, clientY];
    },
  },

  emits: ["messageSeen", "removeMsg", "editMsg"],

  components: {
    ImagesSlide: defineAsyncComponent(() =>
      import("@/components/Media/Slides/ImagesSlide.vue")
    ),
    AudiosList: defineAsyncComponent(() =>
      import("@/components/Media/List/AudiosList.vue")
    ),
    VideosSlide: defineAsyncComponent(() =>
      import("@/components/Media/Slides/VideosSlide.vue")
    ),
    ContextMenu,
  },
  inheritAttrs: false,
};
</script>

<style scoped>
.msg-root {
  @apply relative rounded-md;
}
.chat-context {
  @apply bg-base-200;
}

.chat {
  @apply py-0 relative;
}

.message-context {
  @apply fixed w-40;
}

.chat-bubble {
  @apply break-words max-w-[min(theme(maxWidth.xl),100%)];
}

.files-wrapper {
  @apply my-2 rounded-2xl overflow-hidden;
}

.files-wrapper > :deep(:is(.dynamic-flex, .dynamic-grid)) {
  --min-size: 200px;
  --repeat-mode: auto-fit;
  @apply gap-0.5;
}

.files-wrapper > :deep(:is(.dynamic-flex, .dynamic-grid) > *) {
  @apply min-h-[250px] max-h-[300px];
}

.load-anim::after {
  @apply loading-spinner text-inherit min-w-[20px];
}
</style>
