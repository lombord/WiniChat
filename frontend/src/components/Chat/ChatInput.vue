<template>
  <div class="root-box">
    <div v-if="tmpFile.url" class="prev-box">
      <div class="prev-wrap">
        <img
          class="max-h-[inherit] h-full object-center rounded-xl object-cover"
          v-if="tmpFile.file_type == 'image'"
          :src="tmpFile.url"
          alt=""
        />
        <div
          v-else-if="tmpFile.file_type == 'video'"
          class="rounded-xl overflow-hidden h-full"
        >
          <video
            @loadedmetadata="rewindVideo"
            class="object-center object-cover h-full"
            :src="tmpFile.url"
          />
        </div>
        <button
          @click="resetFile"
          class="btn btn-secondary px-2 py-1.5 rounded-full absolute -top-2 -right-2"
        >
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
    </div>
    <div class="input-box">
      <slot name="top"></slot>
      <form class="s-form" @submit.prevent.stop="submitted">
        <TInput
          @keydown.stop
          v-model="message.content"
          class="s-input peer"
          placeholder="Type Something..."
        />
        <button
          class="s-btn peer/btn"
          type="submit"
          :class="{ 'text-secondary': iVal }"
        >
          <i class="fa-solid fa-arrow-up"></i>
        </button>
        <div class="context-box">
          <FileInput @selected="fileSelected" :accept="this.currentExt">
            <template #default="{ callback }">
              <ContextMenu
                @chosen="callback"
                class="context-m"
                v-model:show="show"
                :menu="menu"
              />
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
import TInput from "@/components/forms/TInput.vue";
import FileInput from "@/components/forms/FileInput.vue";
import ContextMenu from "@/components/UI/ContextMenu.vue";

export default {
  data: () => ({
    show: false,
    currentExt: null,
    tmpFile: null,
  }),
  props: {
    message: {
      type: Object,
      required: true,
    },
  },
  computed: {
    iVal() {
      return !!this.$attrs.modelValue;
    },
    menu() {
      return [
        { label: "Image", cb: this.imageSelect },
        { label: "Video", cb: this.videoSelect },
      ];
    },
  },

  created() {
    this.resetFile();
  },

  methods: {
    imageSelect() {
      this.currentExt = [".png", ".jpg", ".jpeg", ".gif"];
      this.tmpFile.file_type = "image";
    },

    videoSelect() {
      this.currentExt = [
        ".mp4",
        ".mkv",
        ".avi",
        ".mov",
        ".webm",
        ".m4v",
        ".mpg",
        ".mpeg",
      ];
      this.tmpFile.file_type = "video";
    },

    resetFile() {
      this.tmpFile = {
        url: null,
        file_type: null,
        file_name: null,
      };
      this.message.file = null;
      this.currentExt = null;
    },

    fileSelected([file]) {
      this.message.file = file;
      this.tmpFile.url = URL.createObjectURL(file);
    },

    rewindVideo({ target }) {
      target.currentTime = target.duration / 2;
    },

    submitted() {
      this.$emit("submit", this.tmpFile, this.resetFile);
    },
  },
  emits: ["chosen", "selected", "submit"],
  components: { TInput, FileInput, ContextMenu },
};
</script>

<style scoped>
.root-box {
  @apply sticky bottom-0 z-10;
}

.prev-box {
  @apply p-2 flex max-w-4xl mx-auto;
}

.prev-wrap {
  @apply max-h-40 relative aspect-square;
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
  -translate-y-36 right-10 w-[200px];
}

.file-btn {
  @apply btn-ghost py-3 px-3.5
  text-xl text-base-content/60
  hover:text-secondary
  z-10 rounded-full;
}
</style>
