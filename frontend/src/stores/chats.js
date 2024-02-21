import { defineStore } from "pinia";

// store to control common chat actions
export const useChatsStore = defineStore("chats", {
  state: () => ({
    chatsMap: new Map(),
    current: null,
  }),

  getters: {
    currKey() {
      const { current } = this;
      return current && this.getChatKey(current);
    },
  },

  actions: {
    getKey(type, id) {
      return `${type}:${id}`;
    },

    getChatKey(chat) {
      return this.getKey(chat.type, chat.id);
    },

    add(chat) {
      const key = this.getChatKey(chat);
      if (!this.chatsMap.has(key)) {
        this.chatsMap.set(key, chat);
      }
    },

    addCurrent(chat) {
      const key = this.getChatKey(chat);
      const { chatsMap } = this;
      if (!chatsMap.has(key)) {
        chatsMap.set(key, chat);
      }
      this.current = chatsMap.get(key);
    },

    has(type, id) {
      if (!(type && id)) return false;
      const key = this.getKey(type, id);
      return this.chatsMap.has(key);
    },

    hasChat(chat) {
      return this.has(chat.type, chat.id);
    },

    get(type, id) {
      const key = this.getKey(type, id);
      return this.chatsMap.get(key);
    },

    changeCurr(type, id) {
      this.current = this.get(type, id);
    },

    remove(type, id) {
      const key = this.getKey(type, id);
      this.chatsMap.delete(key);
      if (key === this.currKey) {
        this.current = null;
      }
    },

    removeChat(chat) {
      this.remove(chat.type, chat.id);
    },
  },
});
