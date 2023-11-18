<template>
  <div
    @fullscreenchange="updateFS"
    class="root-box"
    :class="{ 'full-screen': fullScreen }"
  >
    <video
      @play="paused = false"
      @pause="paused = true"
      @timeupdate="timeChanged"
      @durationchange="durationChanged"
      @volumechange="volumeChanged"
      ref="videoElm"
      class="video-tag"
      :src="src"
    ></video>
    <div @click="toggleState" class="toggle-box">
      <button class="btn toggle-btn" :class="{ 'toggle-visible': paused }">
        <i v-if="ended" class="fa-solid fa-rotate-right"></i>
        <i v-else-if="paused" class="fa-solid fa-play"></i>
        <i v-else class="fa-solid fa-pause"></i>
      </button>
    </div>
    <div class="video-bottom-box">
      <div class="bottom-content">
        <RangeSlider
          ref="videoRange"
          @input="updateCurrent"
          :min="0"
          :max="duration"
          :range="10"
          v-model="currentTime"
          class="w-full"
        />
        <div class="bottom-items">
          <div>
            {{ timeFormat }}
          </div>
          <div class="center-items-root">
            <div class="pointer-events-auto">
              <button @click="rewind(-5)" class="media-btn btn">
                <i class="fa-solid fa-clock-rotate-left"></i>
              </button>
              <button
                @click="toggleState"
                class="media-btn btn px-3 py-2.5 text-2xl"
              >
                <i v-if="paused" class="fa-solid fa-play"></i>
                <i v-else class="fa-solid fa-pause px-[1.5px]"></i>
              </button>
              <button @click="rewind(5)" class="media-btn btn">
                <i class="fa-solid fa-clock-rotate-left fa-flip-horizontal"></i>
              </button>
            </div>
          </div>
          <div class="flex">
            <div class="vol-box">
              <button @click="toggleMute" class="media-btn btn p-2 py-2.5">
                <i v-if="muted" class="fa-solid fa-volume-xmark"></i>
                <i v-else class="fa-solid fa-volume-high"></i>
              </button>
              <RangeSlider
                v-model="volume"
                class="vol-range"
                :min="0"
                :max="100"
              />
            </div>
            <button @click="toggleFullScreen" class="media-btn btn">
              <i
                v-if="fullScreen"
                class="fa-solid fa-compress px-[0.15rem]"
              ></i>
              <i v-else class="fa-solid fa-expand"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import moment from "moment";
import RangeSlider from "./RangeSlider.vue";

export default {
  data: () => ({
    paused: true,
    currentTime: 0,
    duration: 0,
    fullScreen: false,
  }),

  props: {
    src: {
      type: String,
      required: true,
    },
  },

  computed: {
    videoElm() {
      return this.$refs.videoElm;
    },

    videoRangeElm() {
      return this.$refs.videoRange.$el;
    },

    playing() {
      return !this.paused;
    },

    ended() {
      return this.duration - this.currentTime < 1;
    },

    durationMom() {
      return this.getMoment(Math.round(this.duration * 1e3));
    },

    format() {
      return this.durationMom.hour() >= 1 ? "h:mm:ss" : "m:ss";
    },

    timeFormat() {
      const current = this.getMoment(Math.round(this.currentTime * 1e3));
      const duration = this.durationMom;
      const format = this.format;
      return `${current.format(format)}/${duration.format(format)}`;
    },

    muted: {
      get() {
        return this.$media.muted;
      },
      set(val) {
        this.$media.muted = val;
      },
    },

    volume: {
      get() {
        return this.$media.volume;
      },
      set(val) {
        this.$media.volume = val <= 0 ? 0 : val >= 100 ? 100 : val;
      },
    },
  },

  mounted() {
    this.paused = this.videoElm.paused;
    this.videoElm.volume = this.volume / 100;
  },

  methods: {
    play() {
      this.videoElm.play();
      const prev = this.$media.currentMedia;
      this.$media.currentMedia = this;
      if (prev && prev !== this) {
        prev.pause();
      }
    },

    pause() {
      this.videoElm.pause();
    },

    toggleState() {
      if (this.paused) this.play();
      else this.pause();
    },

    getMoment(ms) {
      const result = moment(0);
      result.hours(0);
      result.milliseconds(ms);
      return result;
    },

    rewind(num) {
      let result = this.currentTime + num;
      if (result >= this.duration) {
        result = this.duration;
      } else if (result <= 0) {
        result = 0;
      }
      this.videoElm.currentTime = result;
    },

    toggleMute() {
      this.muted = !this.muted;
    },

    updateCurrent({ target: { value } }) {
      this.videoElm.currentTime = value;
    },

    updateVolume(value) {
      this.videoElm.volume = value / 100;
    },

    timeChanged({ target: { currentTime } }) {
      this.currentTime = Math.floor(currentTime);
    },

    volumeChanged() {
      this.volume = this.videoElm.volume * 100;
    },

    durationChanged() {
      this.duration = this.videoElm.duration;
    },

    updateFS() {
      this.fullScreen = document.fullscreenElement;
    },

    async toggleFullScreen() {
      if (!document.fullscreenElement) {
        await this.$el.requestFullscreen();
      } else if (document.exitFullscreen) {
        await document.exitFullscreen();
      }
    },
  },

  watch: {
    volume(val) {
      this.updateVolume(val);
    },
    muted(val) {
      this.videoElm.muted = val;
    },
  },

  components: { RangeSlider },
};
</script>

<style scoped>
/* Root styles */
.root-box {
  @apply relative rounded-2xl overflow-hidden text-white/80;
}

.video-tag {
  @apply w-full h-full;
}

.full-screen {
  @apply fixed rounded-none bg-black m-0
  inset-0 max-h-none z-[1000] !important;
}

/* Toggle btn styles */
.toggle-box {
  @apply absolute inset-0 flex justify-center 
  items-center;
}

.toggle-btn {
  @apply btn-ghost text-4xl rounded-full
  px-10 py-5 btn-square transition text-white;
  animation: 0.4s linear 0.1s 1 forwards fade;
}

.full-screen .toggle-btn {
  @apply text-6xl px-[3.2rem];
}

.toggle-box:active .toggle-btn {
  @apply opacity-0 !important;
  animation: 0;
}

.toggle-visible {
  @apply opacity-100;
  animation-fill-mode: backwards;
  animation-direction: reverse;
  animation-delay: 0s;
}

@keyframes fade {
  0% {
    @apply opacity-100;
  }

  50% {
    @apply opacity-0 scale-[200%];
  }

  100% {
    @apply opacity-0;
  }
}

.toggle-btn:hover {
  @apply opacity-100 scale-100 !important;
}

.video-bottom-box {
  @apply z-10 absolute pointer-events-none
  bottom-0 inset-x-0 px-4 pb-2 pt-10 
  duration-300 opacity-0
  bg-gradient-to-t from-[rgba(0,0,0,0.5)] to-transparent;
}

.video-bottom-box:hover {
  @apply transition-none opacity-100;
}

/* bottom styles */
.bottom-content {
  @apply pointer-events-auto;
}

.bottom-items {
  @apply flex items-center justify-between relative;
}

.full-screen .bottom-items {
  @apply my-2;
}

.media-btn {
  @apply btn-ghost text-lg p-2.5 rounded-full;
}

.center-items-root {
  @apply absolute inset-x-0 flex 
  justify-center items-center pointer-events-none;
}

.vol-box {
  @apply relative flex justify-center gap-1 mr-1 items-center;
}

.vol-range {
  @apply w-14 opacity-0 absolute 
  -rotate-90 -translate-y-12 shadow;
}

.full-screen .vol-range {
  @apply relative transform-none w-20 opacity-100;
}

.vol-box:hover .vol-range {
  @apply opacity-100;
}
.vol-range::-webkit-slider-thumb {
  @apply transform-none !important;
}

.vol-range::-moz-range-thumb {
  @apply transform-none !important;
}
</style>
