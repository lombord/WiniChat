// global store for flash messages

import { defineStore } from "pinia";

export const useFlashesStore = defineStore("flashes", {
  state: () => ({
    // flash messages array
    messages: [],
    _id: 1,
    // default timeout for each message
    timeout: 4e3,
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
    alertMessage(message, code, timeout) {
      timeout = timeout || this.timeout;
      const id = this._id++;
      this.messages.push({ id: id, message, code });
      setTimeout(() => this.removeFlash(id), timeout);
      return id;
    },

    /**
     * Alerts success message
     * @param {String} message - message to alert
     */
    success(message) {
      return this.alertMessage(message, "success");
    },

    /**
     * Alerts info message
     * @param {String} message - message to alert
     */
    info(message) {
      return this.alertMessage(message, "info");
    },

    /**
     * Alerts warning message
     * @param {String} message - message to alert
     */
    warning(message) {
      return this.alertMessage(message, "warning");
    },

    /**
     * Alerts error message
     * @param {String} message - message to alert
     */
    error(message) {
      return this.alertMessage(message, "error");
    },

    /**
     * Alerts messages with given code and timeout
     * @param {String[]} messages - messages to alert
     * @param {String | Number} code - message code
     * @param {Number} timeout - timeout in milliseconds
     */
    alertMessages(messages, code, timeout) {
      messages.forEach(([message, cd]) =>
        this.alertMessage(message, cd || code, timeout)
      );
    },

    /**
     * Alerts error messages with given code and timeout
     * @param {String[]} messages - error messages to alert
     */
    errors(messages) {
      messages.forEach((msg) => this.error(msg));
    },

    /**
     * Removes message with given id
     * @param {Number} id - message id to remove
     */
    removeFlash(id) {
      this.messages.length <= 1 || (this._id = 1);
      if (!this.messages.length) return;
      this.messages.splice(
        this.messages.findIndex((flash) => flash.id == id),
        1
      );
    },
  },
});
