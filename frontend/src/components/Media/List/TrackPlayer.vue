<template>
  <div class="player-root">
    <div class="controls-box">
      <div class="left-box gap-3 overflow-hidden">
        <button @click="playPrevious" class="control-btn btn">
          <i class="fa-solid fa-backward"></i>
        </button>
        <button
          @click="toggleState"
          class="control-btn btn spinner-on-load"
          :class="{ 'load-anim': loading }"
        >
          <span class="toggle-icons">
            <i v-if="ended" class="fa-solid fa-rotate-right"></i>
            <i v-else-if="paused" class="fa-solid fa-play"></i>
            <i v-else class="fa-solid fa-pause"></i>
          </span>
        </button>
        <button @click="playNext" class="control-btn btn">
          <i class="fa-solid fa-forward"></i>
        </button>
      </div>
      <div class="flex-1 w-0 overflow-hidden truncate">
        <p>
          {{ trackName }}
        </p>
      </div>
      <div class="right-box">
        <VolumeSlider
          v-model:volume="volume"
          :muted="muted"
          :toggleMute="toggleMute"
        />
        <button
          @click="toggleRepeat"
          class="control-btn"
          :class="{ 'control-btn-active': repeat }"
        >
          <i class="bi bi-repeat text-xl"></i>
        </button>
        <button
          @click="$emit('update:shuffle', !shuffle)"
          class="control-btn"
          :class="{ 'control-btn-active': shuffle }"
        >
          <i class="bi bi-shuffle"></i>
        </button>
        <button
          @click="toggleShow"
          class="control-btn"
          :class="{ 'control-btn-active': showList }"
        >
          <i class="fa-solid fa-bars"></i>
        </button>
        <button
          @click="$emit('close')"
          class="control-btn hover:text-secondary"
        >
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
    </div>
    <div class="flex items-center gap-1">
      <div class="text-sm w-7">
        {{ currFormat }}
      </div>
      <MediaSlider
        @input="updateCurrent"
        :buffered="buffered"
        :duration="duration"
        v-model="currentTime"
        class="audio-range"
      />
      <div class="text-sm">
        {{ durFormat }}
      </div>
    </div>
    <MediaTag
      tag="audio"
      @loadeddata="dataLoaded"
      ref="mediaElm"
      class="hidden"
    />
  </div>
</template>

<script>
import MediaSlider from "../Utils/MediaSlider.vue";
import VolumeSlider from "../Utils/VolumeSlider.vue";
import MediaView from "../MediaView.vue";
import MediaTag from "../MediaTag.vue";

export default {
  props: {
    repeat: {
      type: Boolean,
      required: true,
    },
    shuffle: {
      type: Boolean,
      required: true,
    },
    showList: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    trackName() {
      const { author, title } = this.metadata;
      if (!(author || title)) {
        return this.metadata.file_name;
      }
      return `${author} - ${title}`;
    },
  },

  mounted() {
    this.$tracks.component = this;
  },
  unmounted() {
    this.$tracks.component = null;
  },

  methods: {
    playPrevious() {
      this.$emit("previous");
    },
    playNext() {
      this.$emit("next");
    },
    toggleRepeat() {
      this.$emit("update:repeat", !this.repeat);
    },
    toggleShow() {
      this.$emit("update:showList", !this.showList);
    },
    dataLoaded() {
      this.play();
    },
  },

  watch: {
    async ended(val) {
      if (val && !this.repeat) {
        this.$emit("next");
      }
    },
    repeat(val) {
      this.mediaElm.loop = val;
    },
    current() {
      this.play();
    },
  },
  emits: [
    "previous",
    "next",
    "close",
    "update:showList",
    "update:repeat",
    "update:shuffle",
  ],
  extends: MediaView,
  components: { MediaTag, MediaSlider, VolumeSlider },
};
</script>

<style scoped>
.player-root {
  @apply px-3 pt-1 border-b border-base-content/10;
}

.player-root::before {
  @apply content-[''] 
  inset-0 -z-10 absolute
  bg-base-300/80 backdrop-blur-md;
}

.control-btn {
  @apply opacity-80 text-primary text-lg p-0 w-6 
  border-none bg-transparent;
}

.control-btn:hover {
  @apply opacity-100;
}

.control-btn-active {
  @apply opacity-100 text-secondary;
}

.toggle-icons {
  @apply w-3.5 flex text-xl justify-center;
}

.controls-box {
  @apply flex items-center gap-2;
}

.left-box,
.right-box {
  @apply flex gap-1 items-center;
}

.time-box {
  @apply flex gap-2 items-center justify-between;
}

.range-time {
  @apply text-sm;
}

.audio-range {
  @apply flex-1 block;
}

:deep(.vol-range) {
  @apply outline outline-1 outline-base-content/10;
  --color1: theme(colors.primary);
}

:deep(.vol-btn) {
  @apply control-btn;
}

.repeat-btn {
  @apply text-secondary;
}
</style>
