<template>
  <div class="relative">
    <TrackPlayer
      ref="player"
      @previous="previous"
      @next="next"
      @close="files = []"
      class="relative z-10 pointer-events-auto"
      :file="current"
      v-model:showList="showList"
      v-model:repeat="repeat"
      v-model:shuffle="shuffle"
    />
    <Transition name="fade">
      <div class="tracks-box" v-if="showList">
        <TracksList
          :files="files"
          :currIdx="currIdx"
          :playing="playing"
          @playTrack="playTrack"
        />
      </div>
    </Transition>
  </div>
</template>

<script>
import slideMixin from "../Slides/slideMixin.js";

import TrackPlayer from "./TrackPlayer.vue";
import TracksList from "./TracksList.vue";
let slideMixin2 = { ...slideMixin };
delete slideMixin2.props;

export default {
  data: () => ({
    showList: false,
    repeat: false,
    shuffle: false,
  }),

  computed: {
    playerComp() {
      return this.$refs.player;
    },
    playing() {
      return this.playerComp.playing;
    },

    files: {
      get() {
        return this.$tracks.files;
      },
      set(tracks) {
        this.$tracks.files = tracks || [];
      },
    },

    currIdx: {
      get() {
        return this.$tracks.currIdx;
      },
      set(index) {
        this.$tracks.currIdx = this.validateIdx(index);
      },
    },
  },

  methods: {
    previous() {
      if (this.shuffle) {
        this.playRandom();
        return;
      }
      if (!this.currIdx) {
        this.currIdx = this.maxIdx;
        return;
      }
      this.currIdx--;
    },

    next() {
      if (this.shuffle) {
        this.playRandom();
        return;
      }
      if (this.isLast) {
        this.currIdx = 0;
        return;
      }
      this.currIdx++;
    },

    playRandom() {
      if (this.length <= 1) {
        return;
      }
      const oldIdx = this.currIdx;
      do {
        this.currIdx = this.$utils.randInt(this.length);
      } while (this.currIdx == oldIdx);
    },

    playTrack(idx) {
      if (this.currIdx == idx) {
        this.playerComp.toggleState();
        return;
      }
      this.currIdx = idx;
    },
  },

  mixins: [slideMixin2],
  components: { TrackPlayer, TracksList },
};
</script>

<style scoped>
.tracks-box {
  @apply p-1 pointer-events-none absolute inset-x-0 flex justify-end;
}
</style>
