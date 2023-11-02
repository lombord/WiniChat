// Main session module that controls
// all requests and responses from the client.

import { defineStore } from "pinia";
import axios from "axios";
import { request } from "../plugins/request.js";

/**
 * Class that handles communication between server and session using
 * WS(WebSocket) protocol
 */
class SessionSocket {
  // endpoint to connect to
  endpoint = "ws://localhost:6969/ws/session/";

  /**
   * Initializes SessionSocket instance.
   * @param {String} token - User token. Used to connect to server
   */
  constructor(token) {
    // WebSocket object
    this._socket = new WebSocket(`${this.endpoint}?token=${token}`);
    // chat event listeners
    this.chatEvents = {};
    // User event listeners
    this.userEvents = {};
    // on message call base message handler method
    this.onWS("message", (...args) => this.onMessage(...args));
  }

  /**
   * Base method that adds listener to WS object.
   * @param {String} type - event type as string.
   * @param {Function} callback - callback to call when event is occurred.
   * @param {Object} options - other event setup options.
   */
  onWS(type, callback, options) {
    this._socket.addEventListener(
      type,
      (ev) => {
        const data = JSON.parse(ev.data || "null");
        callback(data, ev);
      },
      options
    );
  }

  /**
   * Base message event handler.
   *
   * Calls message event handler based on event type
   */
  onMessage({ event_type, event, data }, wsEvent) {
    try {
      this[`${event_type}Message`](event, data, wsEvent);
    } catch (error) {
      console.log(error);
    }
  }

  /**
   * Base method to call listeners of an event from dict.
   */
  callListeners(dict, event, data) {
    const listeners = dict[event];
    if (!listeners) return;
    for (const cb of listeners) cb(data);
  }

  /**
   * User related events handler.
   */
  userMessage(event, data) {
    this.callListeners(this.userEvents, event, data);
  }

  /**
   * Chat related events handler.
   */
  chatMessage(event, data) {
    this.callListeners(this.chatEvents, event, data);
  }

  _addOrCreate(obj, key, value) {
    (obj[key] || (obj[key] = new Set())).add(value);
  }

  /**
   * Adds listener for chat related events
   * with given event.
   */
  onChat(event, callback) {
    this._addOrCreate(this.chatEvents, event, callback);
  }

  /**
   * Adds listener for user related events
   * with given event.
   */
  onUser(event, callback) {
    this._addOrCreate(this.userEvents, event, callback);
  }

  /**
   * Called to track events of a user.
   * @param {Any} user_id - user to track.
   * @param {Function} jointCB - callback to call when user has just joint.
   * @param {Function} leftCB - callback to call when user has left.
   */
  watchUser(user_id, jointCB, leftCB) {
    this.send({
      event: "watch_user",
      user_id,
    });
    this.onUser(`${user_id}_joint`, jointCB);
    this.onUser(`${user_id}_left`, leftCB);
  }

  /**
   * Called to top tracking events of a user.
   * @param {Any} user_id - user to stop tracking.
   * @param {Function} jointCB - join callback used to call watchUser.
   * @param {Function} leftCB - left callback used to call watchUser.
   */
  leaveUser(user_id, jointCB, leftCB) {
    this.send({
      event: "leave_user",
      user_id,
    });
    this.removeUserEvent(`${user_id}_joint`, jointCB);
    this.removeUserEvent(`${user_id}_left`, leftCB);
  }

  // base method to remove an event CB from dict
  _removeEvent(dict, event, callback) {
    try {
      dict[event].remove(callback);
    } catch (error) {}
  }

  // method to remove user event CB
  removeUserEvent(event, callback) {
    this._removeEvent(this.userEvents, event, callback);
  }

  // method to remove chat event CB
  removeChatEvent(event, callback) {
    this._removeEvent(this.chatEvents, event, callback);
  }

  /**
   * Base method to join a Chat to track chats events form server.
   * @param {Any} chat_id - chat to join.
   * @param {Function} callback - callback to call when sent a new message.
   */
  joinChat(chat_id, callback) {
    this.send({ event: "join_chat", chat_id });
    this.onChat(`${chat_id}_message`, callback);
  }

  /**
   * Base method to leave a Chat.
   * @param {Any} chat_id - chat to leave.
   * @param {Function} callback - cb used when joint the chat.
   */
  leaveChat(chat_id, callback) {
    this.send({ event: "leave_chat", chat_id });
    this.removeChatEvent(`${chat_id}_message`, callback);
  }

  // Base method to send message to server
  send(data) {
    this._socket.send(JSON.stringify(data));
  }

  sendEvent(event, options) {
    options || (options = {});
    this.send({ event, ...options });
  }

  // Base method to send chat message
  sendChat(chat_id, data) {
    this.send({ event: "send_chat", chat_id, data });
  }

  // called to close connection with server
  close(code) {
    this._socket.close(code);
  }
}

// session store that contains all session info such as
// token, user, socket, etc.
// Controls interaction with server.
export const useSessionStore = defineStore("session", {
  state: () => ({
    // token to get access to server
    access: "",
    // refresh token to update the access token
    refresh: "",
    // Session user object
    user: undefined,
    // session socket object
    socket: null,
  }),

  getters: {
    // property that defines if user is authenticated
    isAuthenticated: (state) => {
      return !!state.user;
    },
    // property that defines if session is loaded
    isLoaded: (state) => {
      return state.user !== undefined;
    },

    // wraps axios request object with session headers
    tRequest(state) {
      const { defaults } = request;
      const conf = {
        headers: { Authorization: `Bearer ${state.access}` },
      };
      return axios.create({ ...defaults, ...conf });
    },
  },

  actions: {
    /**
     * Animates elm with given class and awaits promise.
     * @param {Promise} promise - promise to await
     * @param {HTMLElement} elm - elm to animate
     * @param {String} class name to animate with.
     */
    async animate(promise, elm, cls = "load-anim") {
      elm = elm || document.body;
      elm.classList.add(cls);
      try {
        // just for a longer animation
        await new Promise((r) => setTimeout(r, 100));
        return await promise;
      } finally {
        elm.classList.remove(cls);
      }
    },

    /**
     * Update given fields of a user to server.
     */
    async patchFields(...fields) {
      const data = Object.fromEntries(fields.map((k) => [k, this.user[k]]));
      return await this.patch("session/update/", data);
    },

    /**
     * Fetches token from server based on data.
     * Data should contain authentication credentials
     * @param {Object} data - authentication credentials.
     */
    async fetchToken(data) {
      const response = await request.post("token/", data);
      this.$patch(response.data);
    },

    /**
     * Updates access token using refresh token.
     *
     * If any error occurs during update user will be logged out
     */
    async updateToken() {
      let response;
      const data = { refresh: this.refresh };
      try {
        response = await request.post("token/refresh/", data);
        this.$patch(response.data);
        return true;
      } catch (err) {
        this.logout();
      }
    },

    /**
     * Base request method that controls requests related with token.
     *
     * If any error occurs during request and it is related with token
     * it will try to refresh token
     *
     * if it doesn't work user will be logged out,
     * otherwise request will be sent again
     * @param {Object} config - request config object same as axios config.
     */
    async request(config) {
      this.access || (this.access = "123");
      try {
        return await this.tRequest.request(config);
      } catch (err) {
        const code = err.response.data.code;
        console.log(code);
        if (code === "token_not_valid") {
          const isUpdated = await this.updateToken();
          if (isUpdated) {
            return await this.request(config);
          }
        }
        if (code === "user_not_found") {
          return this.logout();
        }
        throw err;
      }
    },

    /**
     * Merges two objects.
     */
    update(old, new_) {
      old || (old = {});
      return { ...old, ...new_ };
    },

    /**
     * Sends get request to a url.
     * @param {String} url - url to send request
     * @param {Object} config - request configuration
     * @return {Promise} Returns promise.
     */
    get(url, config) {
      (config || (config = {})).url = url;
      return this.request(config);
    },

    /**
     * Sends delete request to a url.
     * @param {String} url - url to send request
     * @param {Object} config - request configuration
     * @return {Promise} Returns promise.
     */
    delete(url, config) {
      (config || (config = {})).url = url;
      config.method = "delete";
      return this.request(config);
    },

    /**
     * Base method for requests with body (post, put, patch, etc.).
     * @param {String} method - request method
     * @param {String} url - url to send request
     * @param {Object} config - request configuration
     * @return {Promise} Returns promise.
     */
    dataRequest(method, url, data, config) {
      const _new = { url, data, method };
      return this.request(this.update(config, _new));
    },

    /**
     * Method to send post request extends 'dataRequest' function
     * @return {Promise} Returns promise.
     */
    post(...args) {
      return this.dataRequest("post", ...args);
    },

    /**
     * Method to send put request extends 'dataRequest' function
     * @return {Promise} Returns promise.
     */
    put(...args) {
      return this.dataRequest("put", ...args);
    },

    /**
     * Method to send patch request extends 'dataRequest' function
     * @return {Promise} Returns promise.
     */
    patch(...args) {
      return this.dataRequest("patch", ...args);
    },

    /**
     * Fetches session user data from the server
     */
    async fetchUser() {
      try {
        const response = await this.get("session/");
        this.user = response.data;
      } catch (err) {
        this.user = null;
        throw err;
      }
    },

    /**
     * Base method to load session.
     */
    async loadSession() {
      this.loadFromLocalStore();
      try {
        await this.fetchUser();
      } catch (err) {
        console.log(err);
      }
    },

    /**
     * Loads session tokens from local storage.
     */
    loadFromLocalStore() {
      this.refresh = localStorage.getItem("refresh") || "";
      this.access = localStorage.getItem("access") || "";
    },

    /**
     * Base method to login user.
     */
    async login(data) {
      await this.fetchToken(data);
      await this.animate(this.fetchUser());
    },

    /**
     * Base method to logout user.
     */
    logout() {
      this.user = null;
      localStorage.clear();
      try {
        this.socket.close();
      } catch (error) {}
      this.$reset();
    },

    /**
     * Connects to the server using WebSocket protocol.
     */
    connectServer(callback) {
      this.socket = new SessionSocket(this.access);
      this.socket.onWS("open", callback);
    },
  },
});

const sessionStore = useSessionStore();

// tracks changes of session store if access or refresh changes
// its state it will be updated on local storage too.
sessionStore.$subscribe((mutation, state) => {
  if (!state) return;
  const { access, refresh } = state;
  access && localStorage.setItem("access", state.access);
  refresh && localStorage.setItem("refresh", state.refresh);
});
