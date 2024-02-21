<template>
  <div
    @fullscreenchange="updateFS"
    class="root-box z-0"
    :class="{ 'full-screen': fullScreen }"
    :style="{ '--videoUrl': `url(${url})` }"
  >
    <MediaTag
      ref="mediaElm"
      tag="video"
      @loadedmetadata="resizeCV"
      @play="drawBG"
      @loadeddata="play"
      class="video-tag"
    />
    <canvas ref="canvas" class="canvas"></canvas>
    <div
      class="absolute right-2 top-2 z-10 hover:opacity-100"
      :class="{ 'opacity-0': playing }"
    >
      <button
        @click="$session.download(url, file_name)"
        class="icon-btn text-xl py-2.5"
      >
        <i class="bi bi-cloud-download"></i>
      </button>
    </div>
    <div @click="toggleState" class="toggle-box">
      <button
        class="btn toggle-btn"
        :class="{ 'toggle-visible': paused, 'load-anim': loading }"
      >
        <i v-if="ended" class="fa-solid fa-rotate-right"></i>
        <i v-else-if="paused" class="fa-solid fa-play"></i>
        <i v-else class="fa-solid fa-pause"></i>
      </button>
    </div>
    <div class="video-bottom-box">
      <div class="bottom-content">
        <MediaSlider
          @input="updateCurrent"
          :buffered="buffered"
          :duration="duration"
          v-model="currentTime"
        />
        <div class="bottom-items">
          <div>
            {{ defFormat }}
          </div>
          <div class="center-items-root">
            <div class="pointer-events-auto flex gap-1 items-center">
              <button @click="rewind(-5)" class="icon-btn">
                <i class="fa-solid fa-clock-rotate-left"></i>
              </button>
              <button
                @click="toggleState"
                class="icon-btn px-3 py-2.5 text-2xl"
              >
                <i v-if="paused" class="fa-solid fa-play"></i>
                <i v-else class="fa-solid fa-pause px-[1.5px]"></i>
              </button>
              <button @click="rewind(5)" class="icon-btn">
                <i class="fa-solid fa-clock-rotate-left fa-flip-horizontal"></i>
              </button>
            </div>
          </div>
          <div class="flex">
            <div class="vol-box">
              <button @click="toggleMute" class="icon-btn p-2 py-2.5">
                <span class="flex justify-center w-6">
                  <i
                    v-if="muted || !volume"
                    class="fa-solid fa-volume-xmark"
                  ></i>
                  <i
                    v-else-if="volume <= 20"
                    class="fa-solid fa-volume-off"
                  ></i>
                  <i
                    v-else-if="volume <= 60"
                    class="fa-solid fa-volume-low"
                  ></i>
                  <i v-else class="fa-solid fa-volume-high"></i>
                </span>
              </button>
              <RangeSlider
                v-model="volume"
                class="vol-range"
                :min="0"
                :max="100"
              />
            </div>
            <button @click="toggleFullScreen" class="icon-btn">
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
import MediaSlider from "./Utils/MediaSlider.vue";
import RangeSlider from "./Utils/RangeSlider.vue";
import MediaView from "./MediaView.vue";
import MediaTag from "./MediaTag.vue";
export default {
  data: () => ({
    fullScreen: false,
  }),

  computed: {
    canvas() {
      return this.$refs.canvas;
    },

    ctx() {
      return this.canvas.getContext("2d");
    },
  },

  methods: {
    resizeCV({ target }) {
      this.canvas.width = target.videoWidth;
      this.canvas.height = target.videoHeight;
    },

    drawBG() {
      this.ctx.drawImage(this.mediaElm, 0, 0);
      if (!(this.mediaElm.paused || this.mediaElm.ended)) {
        requestAnimationFrame(this.drawBG);
      }
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

  components: { MediaTag, MediaSlider, RangeSlider },
  extends: MediaView,
};
</script>

<style scoped>
/* Root styles */
.root-box {
  @apply relative overflow-hidden text-white/80;
}

.full-screen {
  @apply fixed rounded-none bg-black m-0
  text-lg
  inset-0 max-h-none z-[1000] !important;
}

.video-tag {
  @apply w-full max-h-[inherit] object-contain;
}

.canvas {
  @apply absolute inset-0 
  w-full h-full -z-10 
  blur-lg scale-110
  object-top;
}

.full-screen .video-tag {
  @apply max-h-full;
}

.full-screen .icon-btn {
  @apply text-2xl !important;
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
  -webkit-font-smoothing: subpixel-antialiased;
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

.load-anim {
  @apply animate-none;
}

.load-anim::after {
  @apply w-[70%] text-[inherit];
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
