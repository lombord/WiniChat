// Global store for groups

import { defineStore } from "pinia";

export const useGroupStore = defineStore("group", {
  state: () => ({
    showSettings: false,
  }),

  actions: {},
});
