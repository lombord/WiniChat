<template>
  <div></div>
</template>

<script>
import moment from "moment";
import fileMixin from "@/mixins/fileMixin.js";

export default {
  data: () => ({
    paused: true,
    currentTime: 0,
    duration: 0,
    loading: true,
    buffered: 0,
  }),

  computed: {
    mediaElm() {
      return this.$refs.mediaElm;
    },

    playing() {
      return !this.paused;
    },

    ended() {
      return this.duration - this.currentTime < 1;
    },

    durationMom() {
      return moment.utc(this.duration * 1e3);
    },

    currentMom() {
      return moment.utc(this.currentTime * 1e3);
    },

    format() {
      return this.durationMom.hour() >= 1 ? "h:mm:ss" : "m:ss";
    },

    currFormat() {
      return this.currentMom.format(this.format);
    },

    durFormat() {
      return this.durationMom.format(this.format);
    },

    defFormat() {
      return `${this.currFormat}/${this.durFormat}`;
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
    this.paused = this.mediaElm.paused;
    this.mediaElm.volume = this.volume / 100;
  },

  methods: {
    async play() {
      const prev = this.$media.currentMedia;
      if (prev && prev !== this) {
        prev.pause();
      }
      this.$media.currentMedia = this;
      await this.mediaElm.play();
    },

    pause() {
      this.mediaElm.pause();
    },

    toggleState() {
      if (this.paused) this.play();
      else this.pause();
    },

    rewind(num) {
      let result = this.currentTime + num;
      if (result >= this.duration) {
        result = this.duration;
      } else if (result <= 0) {
        result = 0;
      }
      this.mediaElm.currentTime = result;
    },

    toggleMute() {
      this.muted = !this.muted;
    },

    updateCurrent({ target: { value } }) {
      this.mediaElm.currentTime = value;
    },

    updateVolume(value) {
      this.mediaElm.volume = value / 100;
    },

    timeChanged({ target: { currentTime } }) {
      this.currentTime = Math.floor(currentTime);
    },

    volumeChanged() {
      this.volume = this.mediaElm.volume * 100;
    },

    durationChanged() {
      this.duration = this.mediaElm.duration;
    },

    calcProgress() {
      if (this.duration <= 0) return;
      const { buffered, currentTime } = this.mediaElm;
      for (let i = 0; i < buffered.length; i++) {
        let pos = buffered.length - 1 - i;
        if (buffered.start(pos) <= currentTime) {
          this.buffered = ((buffered.end(pos) + 4) * 100) / this.duration;
          return;
        }
      }
    },
  },

  watch: {
    volume(val) {
      this.updateVolume(val);
    },
    muted(val) {
      this.mediaElm.muted = val;
    },
  },

  mixins: [fileMixin],
};
</script>

<style scoped></style>
