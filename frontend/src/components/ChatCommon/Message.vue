<template>
  <div class="msg-root" v-int.show="!isSession && !seen && markMessage">
    <div class="chat gap-2" :class="$attrs.class">
      <div class="chat-bubble">
        <template v-if="files?.length">
          <div class="files-wrapper">
            <DynamicComp :path="path" :files="files">
              <template #fallback>
                <component
                  class="max-w-full w-[36rem]"
                  :is="skeletonComp"
                  :count="files.length"
                />
              </template>
            </DynamicComp>
          </div>
        </template>
        <div class="message">
          {{ message.content }}
        </div>
        <div
          class="h-3 flex opacity-80 text-xs gap-0.5 justify-end items-center"
        >
          <span v-if="!isPosted" class="load-anim spinner-on-load align-middle p-3 ml-2"></span>
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
  </div>
</template>

<script>
import moment from "moment";

import DynamicComp from "@/components/Utils/DynamicComp.vue";
import GridSkeleton from "@/components/Skeletons/GridSkeleton.vue";
import ListSkeleton from "@/components/Skeletons/ListSkeleton.vue";

export default {
  props: {
    owner: {
      type: Object,
      required: true,
    },

    message: {
      type: Object,
      required: true,
    },

    isSession: {
      type: Boolean,
      required: true,
    },
  },

  computed: {
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

    fileType() {
      return this.files[0].file_type;
    },

    path() {
      return this.$options._mediaPath[this.fileType];
    },

    socket() {
      return this.$session.socket;
    },

    skeletonComp() {
      if (this.fileType == "audio") return "ListSkeleton";
      return "GridSkeleton";
    },
  },

  _mediaPath: {
    image: "Media/Slides/ImagesSlide.vue",
    video: "Media/Slides/VideosSlide.vue",
    audio: "Media/List/AudiosList.vue",
  },

  methods: {
    markMessage() {
      this.$emit("msgSeen", this.message);
      return true;
    },
  },

  emits: ["msgSeen"],
  components: {
    DynamicComp,
    GridSkeleton,
    ListSkeleton,
  },
};
</script>

<style scoped>
.msg-root {
  @apply relative rounded-md;
}

.chat {
  @apply py-0 relative;
}

:deep(.message-context) {
  @apply w-[160px];
}

.chat-bubble {
  @apply break-words max-w-[min(theme(maxWidth.xl),100%)];
}

.files-wrapper {
  @apply my-2 rounded-2xl overflow-hidden;
}

.files-wrapper > :deep(.dynamic-flex) {
  --min-size: 200px;
  --repeat-mode: auto-fit;
  @apply gap-0.5;
}

.files-wrapper > :deep(.dynamic-flex > *) {
  @apply min-h-[250px] max-h-[17rem];
}

.files-wrapper :deep(.img-placeholder) {
  @apply max-w-full w-[36rem] min-h-[17rem];
}

.load-anim::after {
  @apply loading-spinner text-inherit;
}
</style>
