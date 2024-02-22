// Global store for user profile 

import { defineStore } from "pinia";

export const useProfileStore = defineStore("profile", {
  state: () => ({
    current: null,
    showProfile: false,
  }),

  actions: {
    show(userId) {
      this.current = userId;
      this.showProfile = true;
    },
  },
});
