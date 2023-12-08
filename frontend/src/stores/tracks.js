import { defineStore } from "pinia";

export const useTracksStore = defineStore("tracks", {
  state: () => ({
    files: [],
    currIdx: 0,
    component: null,
  }),
  getters: {
    isPlaying: (state) => {
      if (!state.component) return false;
      return state.component.playing;
    },
  },
  actions: {
    toggle() {
      try {
        this.component.toggleState();
      } catch (error) {}
    },
  },
});
