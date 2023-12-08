<template>
  <div class="root-box">
    <div v-if="editing || files.length" class="prev-box">
      <div v-if="editing" class="edit-box">
        <div class="flex gap-2 items-center">
          <p
            class="text-primary rounded-full p-2 px-3 text-xl border border-base-content/20"
          >
            <span>
              <i class="fa-solid fa-pen"></i>
            </span>
          </p>
          <div class="">
            {{ ogContent }}
          </div>
        </div>
        <button @click="$emit('cancelEdit')" class="btn x-btn">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
      <div v-else class="files-box">
        <div class="files-prev">
          <div v-for="(file, i) in prevFiles" class="relative">
            <component :is="currComponent" :file="file" class="file-prev" />
            <button @click="removeFile(i)" class="btn x-btn">
              <i class="fa-solid fa-xmark"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="input-box">
      <slot name="top"></slot>
      <form class="s-form" @submit.prevent.stop="submitted">
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
                <template #image>
                  <i class="fa-solid fa-images"></i>
                  <span class="hidden md:inline-block">image</span>
                </template>
                <template #audio>
                  <i class="fa-solid fa-music"></i>
                  <span class="hidden md:inline-block">audio</span>
                </template>
                <template #video>
                  <i class="fa-solid fa-film"></i>
                  <span class="hidden md:inline-block">video</span>
                </template>
              </ContextMenu>
            </template>
          </FileInput>
          <button
            type="button"
            @click.stop.prevent="show = !show"
            class="file-btn btn"
            :class="{ 'text-secondary': show }"
          >
            <i class="fa-solid fa-paperclip"></i>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { defineAsyncComponent } from "vue";

import TInput from "@/components/forms/TInput.vue";
import FileInput from "@/components/forms/FileInput.vue";
import ContextMenu from "@/components/UI/ContextMenu.vue";

export default {
  data: () => ({
    show: false,
    currentExt: null,
    file_type: null,
    ogContent: "",
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
  },
  computed: {
    menu() {
      return [
        { label: "image", cb: this.imageSelect },
        { label: "audio", cb: this.audioSelect },
        { label: "video", cb: this.videoSelect },
      ];
    },
    currComponent() {
      return {
        image: "ImagePreview",
        video: "VideoPreview",
        audio: "AudioPreview",
      }[this.file_type];
    },
    content: {
      get() {
        return this.message.content;
      },
      set(val) {
        return (this.message.content = val);
      },
    },
    files: {
      get() {
        return this.message.files;
      },
      set(val) {
        this.message.files = val;
      },
    },
    prevFiles() {
      return this.files.map((file, i) => {
        let others = {};
        if (this.file_type == "audio") {
          others = { duration: 0 };
          const audioContext = new AudioContext();
          file.arrayBuffer().then((arrBuffer) => {
            try {
              audioContext.decodeAudioData(arrBuffer, (buffer) => {
                this.prevFiles[i].metadata.duration = buffer.duration;
              });
            } catch (error) {}
          });
        }
        return {
          url: URL.createObjectURL(file),
          file_type: this.file_type,
          metadata: {
            file_name: file.name,
            size: file.size,
            ...others,
          },
        };
      });
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
      this.files.splice(index, 1);
    },

    filesSelected(files) {
      if (this.editing) return;
      this.files = [...files];
    },

    submitted() {
      if (this.editing) {
        this.$emit("edited");
      } else {
        this.$emit("submit", this.prevFiles);
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
    ContextMenu,
    ImagePreview: defineAsyncComponent(() => import("./ImagePreview.vue")),
    VideoPreview: defineAsyncComponent(() => import("./VideoPreview.vue")),
    AudioPreview: defineAsyncComponent(() => import("./AudioPreview.vue")),
  },
};
</script>

<style scoped>
.root-box {
  @apply sticky bottom-0 z-10;
}

.prev-box {
  @apply max-w-4xl mx-auto overflow-x-auto;
}

.x-btn {
  @apply btn-secondary px-2 py-1.5 
  rounded-full absolute -top-2 -right-2;
}

.edit-box {
  @apply p-2.5 mb-0.5 bg-base-200/50 border border-base-content/5
  backdrop-blur-xl w-full rounded-md relative;
}

.files-box {
  @apply rounded-xl overflow-auto
  border border-base-content/10 mx-1
  bg-base-300/30 px-3 py-3 backdrop-blur-xl;
}

.files-prev {
  @apply flex gap-2;
}

.files-prev :deep(.file-prev) {
  @apply relative h-52 aspect-square rounded-xl overflow-hidden;
}

.prev.wrap > *[src] {
  @apply max-h-[inherit];
}

.prev-file {
  @apply max-h-28 relative;
}

.input-box {
  @apply text-center p-2 py-2.5 relative;
}

.input-box::before {
  content: "";
  @apply bg-base-100/30 absolute
  backdrop-blur-2xl inset-0 -z-[1];
}

.s-form {
  @apply relative flex items-center 
  max-w-4xl mx-auto z-10;
}

.s-input {
  @apply w-full;
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
  -translate-y-48 right-10 w-[200px];
}

.file-btn {
  @apply btn-ghost py-3 px-3.5
  text-xl text-base-content/60
  hover:text-secondary
  z-10 rounded-full;
}
</style>
