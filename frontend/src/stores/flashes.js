// Global store for flash messages

import { defineStore } from "pinia";

export const useFlashesStore = defineStore("flashes", {
  state: () => ({
    // flash messages array
    messages: new Map(),
    /** @type {Promise} */
    _id: 1,
    cleanerId: null,
    // default timeout for each message
    timeout: 3.5e3,
  }),

  getters: {},

  actions: {
    /**
     * Base alert message method.
     *
     * Alerts message with given code and timeout.
     *
     * @param {String} message - message to alert
     * @param {String | Number} code - message code
     * @param {Number} timeout - timeout in milliseconds
     */
    _alertMessage(message, code, timeout) {
      timeout = timeout || this.timeout;
      const id = this._id++;
      this.messages.set(id, { message, code });
      this.setUpCleaner();
    },

    setUpCleaner() {
      if (!this.cleanerId) {
        const { messages } = this;
        const intervalId = (this.cleanerId = setInterval(() => {
          if (!messages.size) {
            clearInterval(intervalId);
            this.cleanerId = null;
            return;
          }
          const id = messages.keys().next().value;
          this.removeFlash(id);
        }, this.timeout));
      }
    },

    stopCleaner() {},

    isIterable(obj) {
      // checks for null and undefined
      if (obj == null) {
        return false;
      }
      return typeof obj[Symbol.iterator] === "function";
    },

    async alertMessage(messages, code, timeout) {
      if (typeof messages === "string" || !this.isIterable(messages)) {
        messages = [messages];
      }
      for (const msg of messages) {
        this._alertMessage(msg, code, timeout);
        await new Promise((r) => setTimeout(r, 100));
      }
    },

    /**
     * Alerts success message
     * @param {String | String[]} message - message(s) to alert
     */
    success(message) {
      return this.alertMessage(message, "success");
    },

    /**
     * Alerts info message
     * @param {String | String[]} message - message(s) to alert
     */
    info(message) {
      return this.alertMessage(message, "info");
    },

    /**
     * Alerts warning message
     * @param {String | String[]} message - message(s) to alert
     */
    warning(message) {
      return this.alertMessage(message, "warning");
    },

    /**
     * Alerts error message
     * @param {String | String[]} message - message(s) to alert
     */
    error(message = "Something went wrong") {
      return this.alertMessage(message, "error");
    },

    axiosError(error) {
      console.log(error);
      const data = error?.response?.data;
      if (!data || typeof data == "string") {
        this.error("Error occurred while processing the request.");
        return;
      }
      for (let val of Object.values(data)) {
        this.error(val);
      }
    },

    /**
     * Removes message with given id
     * @param {Number} id - message id to remove
     */
    removeFlash(id) {
      const messages = this.messages;
      if (!messages.size) return;
      messages.delete(id);
      if (!messages.size) {
        this._id = 1;
        clearInterval(this.cleanerId);
        this.cleanerId = null;
      }
      return true;
    },
  },
});
