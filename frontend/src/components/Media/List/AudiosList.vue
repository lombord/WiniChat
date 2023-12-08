<template>
  <div class="audios-box">
    <AudioItem
      v-for="(file, i) in files"
      :file="file"
      @playAudio="playAudio(i)"
      :class="{ current: isCurrent && currIdx == i && isPlaying }"
      :key="i"
    />
  </div>
</template>

<script>
import AudioItem from "./AudioItem.vue";
export default {
  props: {
    files: {
      type: Array,
      required: true,
    },
  },

  computed: {
    isCurrent() {
      return this.files == this.$tracks.files;
    },
    currIdx() {
      return this.$tracks.currIdx;
    },
    isPlaying() {
      return this.$tracks.isPlaying;
    },
  },

  methods: {
    playAudio(index) {
      if (this.isCurrent && this.currIdx == index) {
        this.$tracks.toggle();
        return;
      }
      const data = {
        currIdx: index,
      };
      if (!this.isCurrent) {
        data["files"] = this.files;
        this.$tracks.currIdx = 0;
      }
      this.$tracks.$patch(data);
    },
  },

  components: { AudioItem },
};
</script>

<style scoped>
.audios-box {
  @apply flex flex-col gap-1.5;
}
</style>
