<template>
  <div class="root-box">
    <div v-if="(canSend && editing) || hasFiles" class="prev-box">
      <EditPreview
        v-if="editing"
        :content="ogContent"
        @cancel="$emit('cancelEdit')"
      />
      <div v-else class="files-box">
        <div class="files-prev">
          <TransitionGroup name="pop">
            <div
              v-for="({ prevFile }, i) in uploadFiles"
              :key="prevFile.url"
              class="relative"
            >
              <DynamicComp :path="currPath" :file="prevFile" class="file-prev">
                <template #fallback>
                  <div class="file-fallback load-sk"></div>
                </template>
              </DynamicComp>
              <button @click="removeFile(i)" class="btn x-btn center-content">
                <i class="fa-solid fa-xmark"></i>
              </button>
            </div>
          </TransitionGroup>
          <div class="clear-wrap flex justify-center">
            <button class="w-btn clear-btn" @click="clearFiles">Clear</button>
          </div>
        </div>
      </div>
    </div>

    <div class="input-box">
      <Transition name="fade" mode="out-in">
        <form v-if="canSend" class="s-form" @submit.prevent.stop="submitted">
          <TInput
            @keydown.stop
            v-model="content"
            class="s-input peer"
            placeholder="Type Something..."
          />
          <button
            class="s-btn peer/btn"
            type="submit"
            :class="{ 'text-secondary': content }"
          >
            <i class="fa-solid fa-arrow-up"></i>
          </button>
          <div class="context-box">
            <FileInput
              @selected="filesSelected"
              :accept="this.currentExt"
              multiple
            >
              <template #default="{ callback }">
                <ContextMenu
                  @chosen="callback"
                  class="context-m"
                  v-model:show="show"
                  :menu="menu"
                >
                </ContextMenu>
              </template>
            </FileInput>
            <button
              type="button"
              @mouseup.stop.prevent
              @click.stop.prevent="show = !show"
              class="file-btn btn"
              :class="{ 'text-secondary': show }"
            >
              <i class="fa-solid fa-paperclip"></i>
            </button>
          </div>
        </form>
        <div v-else class="hint-box" :class="{ 'load-anim': canSendLoading }">
          {{ hintMessage }}
        </div>
      </Transition>
    </div>
  </div>
</template>

<script>
import { reactive } from "vue";

import TInput from "@/components/Forms/Widgets/TInput.vue";
import FileInput from "@/components/Forms/Widgets/FileInput.vue";
import ContextMenu from "@/components/UI/ContextMenu.vue";
import DynamicComp from "@/components/Utils/DynamicComp.vue";

import EditPreview from "./EditPreview.vue";

export default {
  data: () => ({
    show: false,
    currentExt: null,
    file_type: null,
    ogContent: "",
    uploadFiles: null,
  }),

  props: {
    message: {
      type: Object,
      required: true,
    },
    editing: {
      type: Boolean,
      default: false,
    },
    canSend: {
      type: Boolean,
      default: true,
    },

    canSendLoading: {
      type: Boolean,
      default: false,
    },

    hintMessage: {
      type: String,
      default: "You are not allowed to send messages",
    },
  },

  computed: {
    menu() {
      return [
        {
          label: "image",
          icon: "fa-solid fa-images text-accent",
          cb: this.imageSelect,
        },
        {
          label: "audio",
          icon: "fa-solid fa-music text-secondary",
          cb: this.audioSelect,
        },
        {
          label: "video",
          icon: "fa-solid fa-film text-primary",
          cb: this.videoSelect,
        },
      ];
    },

    currPath() {
      return {
        image: "ChatCommon/ChatInput/ImagePreview.vue",
        video: "ChatCommon/ChatInput/VideoPreview.vue",
        audio: "ChatCommon/ChatInput/AudioPreview.vue",
      }[this.file_type];
    },

    hasFiles() {
      return this.uploadFiles && this.uploadFiles.length;
    },

    content: {
      get() {
        return this.message.content;
      },
      set(val) {
        return (this.message.content = val);
      },
    },
  },

  methods: {
    imageSelect() {
      this.currentExt = [".png", ".jpg", ".jpeg", ".gif"];
      this.file_type = "image";
    },

    audioSelect() {
      this.currentExt = [".mp3", ".ogg", ".wav"];
      this.file_type = "audio";
    },

    videoSelect() {
      this.currentExt = [
        ".mp4",
        ".mkv",
        ".avi",
        ".mov",
        ".wmv",
        ".flv",
        ".webm",
      ];
      this.file_type = "video";
    },

    removeFile(index) {
      const [fileObj] = this.uploadFiles.splice(index, 1);
      URL.revokeObjectURL(fileObj.prevFile.url);
    },

    clearFiles() {
      const { uploadFiles } = this;
      if (uploadFiles) {
        uploadFiles.forEach(({ prevFile: { url } }) =>
          URL.revokeObjectURL(url)
        );
      }
      this.uploadFiles = null;
    },

    filesSelected(files) {
      if (this.editing || !(files || files.length)) return;
      this.clearFiles();
      files = Array.from(files);
      this.uploadFiles = files.map(this.getUploadObj);
    },

    getUploadObj(file) {
      const { file_type } = this;
      let metadata = reactive({
        file_name: file.name,
        size: file.size,
      });
      const url = URL.createObjectURL(file);
      if (file_type == "audio") {
        this.setAudioMeta(metadata, url);
      }
      return {
        prevFile: {
          url,
          file_type,
          metadata,
        },
        file,
      };
    },

    setAudioMeta(meta, url) {
      meta.duration = 0;
      const audio = new Audio(url);
      audio.onloadeddata = () => {
        meta.duration = audio.duration;
      };
    },

    submitted() {
      if (this.editing) {
        this.$emit("edited");
      } else {
        const { uploadFiles } = this;
        let prevFiles = null;
        if (uploadFiles) {
          this.message.files = uploadFiles.map(({ file }) => file);
          prevFiles = uploadFiles.map(({ prevFile }) => prevFile);
        }
        this.$emit("submit", prevFiles);
        this.uploadFiles = null;
      }
    },
  },

  watch: {
    editing(val) {
      if (val) this.ogContent = this.message.content;
    },
  },

  emits: ["submit", "cancelEdit", "edited"],
  components: {
    TInput,
    FileInput,
    EditPreview,
    ContextMenu,
    DynamicComp,
  },
};
</script>

<style scoped>
.root-box {
  @apply sticky bottom-0 z-50;
}

.prev-box {
  @apply absolute bottom-full inset-x-0
  flex justify-center px-2;
}

.prev-box > * {
  @apply max-w-4xl flex-1;
}

.files-box {
  @apply rounded-xl overflow-hidden
  border border-base-content/10 mx-1
  bg-base-300/30 pb-2  backdrop-blur-xl;
}

.files-prev {
  @apply flex gap-2 max-h-44 px-3 py-3 overflow-auto;
}

.file-fallback {
  @apply file-prev p-20 bg-base-content/50 
  aspect-square rounded-2xl;
}

.files-prev :deep(.file-prev:first-child) {
  @apply relative h-40 aspect-square rounded-xl overflow-hidden;
}

.prev.wrap > *[src] {
  @apply max-h-[inherit];
}

.prev-file {
  @apply max-h-28 relative;
}

.x-btn {
  @apply aspect-square bg-base-content
  text-base-100
  border-none rounded-full
  p-2 absolute -top-1.5 -right-1.5;
}

.clear-wrap {
  @apply absolute inset-x-0 bottom-0
  pb-2 pointer-events-none;
}

.clear-btn {
  @apply p-1 opacity-0 scale-0 px-3 text-base
  btn-primary pointer-events-auto;
}

.files-box:is(:hover, :active, :focus) .clear-btn {
  @apply opacity-100 scale-100 active:scale-95;
}

.input-box {
  @apply text-center p-2 relative flex justify-center;
}

.input-box::before {
  content: "";
  @apply absolute
  w-full h-full overflow-hidden
  backdrop-blur-2xl
  inset-0
  -z-[1];
  transform: translate3d(0, 0, 0) skew(0.5deg);
  backface-visibility: hidden;
}

.input-box > * {
  @apply flex-1 w-20 max-w-4xl shrink-0;
}

.input-box > .hint-box {
  @apply truncate;
}

.hint-box {
  @apply p-3 truncate border-2 border-base-content/15 
  bg-base-100 bg-opacity-80 rounded-xl text-base-content/90;
}

.s-form {
  @apply relative flex items-center z-10;
}

.s-input {
  @apply w-full bg-base-100/80 rounded-xl py-3 px-4
  placeholder:text-base-content/60;
}

.s-btn {
  @apply absolute right-3 py-3 px-3.5
  invisible
  rounded-full min-h-fit h-fit
  btn btn-ghost text-lg outline-0
  text-base-content/50
  peer-focus:visible
  active:visible;
}

.context-box {
  @apply peer-focus:hidden
  peer-active/btn:hidden
  absolute right-3 z-10;
}

.context-m {
  @apply bg-black/5
  origin-bottom
  bottom-[calc(100%_+_1rem)] right-0 w-[200px];
}

.file-btn {
  @apply btn-ghost py-3 px-3.5
  text-xl text-base-content/60
  hover:text-secondary
  z-10 rounded-full;
}
</style>
