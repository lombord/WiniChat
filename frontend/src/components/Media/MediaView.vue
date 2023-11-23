<template>
  <div></div>
</template>

<script>
import moment from "moment";

export default {
  data: () => ({
    paused: true,
    currentTime: 0,
    duration: 0,
    loading: false,
    buffered: 0,
  }),
  props: {
    file: {
      type: Object,
      required: true,
    },
  },
  computed: {
    src() {
      return this.file.url;
    },

    file_name() {
      return this.file.file_name || this.src.split("/").reverse()[0];
    },

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
      return this.getMoment(Math.round(this.duration * 1e3));
    },

    format() {
      return this.durationMom.hour() >= 1 ? "h:mm:ss" : "m:ss";
    },

    currentFormat() {
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
    this.paused = this.mediaElm.paused;
    this.mediaElm.volume = this.volume / 100;
  },

  methods: {
    async play() {
      await this.mediaElm.play();
      const prev = this.$media.currentMedia;
      this.$media.currentMedia = this;
      if (prev && prev !== this) {
        prev.pause();
      }
    },

    pause() {
      this.mediaElm.pause();
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
};
</script>

<style scoped></style>
