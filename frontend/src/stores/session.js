// Store that controls communication with server
// using `http(s)` and `ws` protocols

import { ref, reactive, markRaw, shallowReadonly } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { request } from "@/plugins/request.js";

const GroupWSMixin = (Cls = Object) =>
  class extends Cls {
    constructor() {
      super();
      this.groupWS = new Map();
      this.grpGenEvents = new Map();
      this.onGroupGen("role_updated", ({ group_id, role_id, data }) =>
        this.refreshRole(group_id, role_id, data)
      );
      this.onGroupGen("del_role", this.delGroupRole.bind(this));
      this.onGroupGen("remove_members", this.clearMembers.bind(this));
      this.onGroupGen("change_role", this.changeMemberRole.bind(this));
    }

    setUpGroupWS(id) {
      const wsObj = { events: new Map(), roles: new Map(), members: new Map() };
      this.groupWS.set(id, wsObj);
      return wsObj;
    }

    getGroupWS(id, prop) {
      try {
        return this.groupWS.get(id)[prop];
      } catch (error) {}
    }

    acquireGroupWS(id, prop) {
      let result = this.getGroupWS(id, prop);
      if (!result) {
        result = this.setUpGroupWS(id)[prop];
      }
      return result;
    }

    /**
     * Group related events handler.
     */
    groupMessage(event, data) {
      this.groupEventHandler(event, data);
      this.grpGenHandler(event, data);
    }

    getEventListeners(id, event) {
      try {
        return this.groupWS.get(id).events.get(event);
      } catch (error) {}
    }

    groupEventHandler(event, { group_id, data, ...rest }) {
      const listeners = this.getEventListeners(group_id, event);
      if (!listeners) return;
      for (const callback of listeners) {
        callback(data, rest);
      }
    }

    grpGenHandler(event, data) {
      let callback = this.grpGenEvents.get(event);
      if (callback) {
        callback(data);
      }
    }

    onGroupGen(event, callback) {
      this.grpGenEvents.set(event, callback);
    }

    onGroup(id, event, callback) {
      const events = this.acquireGroupWS(id, "events");
      let listeners = events.get(event);
      if (!listeners) {
        listeners = new Set();
        events.set(event, listeners);
      }
      listeners.add(callback);
    }

    getGroupEvents(id) {
      return this.getGroupWS(id, "events");
    }

    getRoles(id) {
      return this.getGroupWS(id, "roles");
    }

    getMembers(id) {
      return this.getGroupWS(id, "members");
    }

    getRole(groupId, roleId) {
      return this.getRoles(groupId)?.get(roleId);
    }

    getMember(groupId, userId) {
      return this.getMembers(groupId)?.get(userId);
    }

    watchRole(groupId, roleId) {
      const roles = this.acquireGroupWS(groupId, "roles");
      let role = roles.get(roleId);
      if (!role) {
        role = ref({ id: roleId });
        roles.set(roleId, role);
      }
      return shallowReadonly(role);
    }

    watchMember(groupId, userId, roleId) {
      const members = this.acquireGroupWS(groupId, "members");
      let member = members.get(userId);
      if (!member) {
        const role = this.watchRole(groupId, roleId);
        member = reactive({ id: userId, role });
        members.set(userId, member);
      }
      return member;
    }

    refreshRole(groupId, roleId, data) {
      let role = this.getRole(groupId, roleId);
      if (role && data) {
        Object.assign(role.value, data);
      }
    }

    changeMemberRole({ group_id, user_id, data: newRole }) {
      const member = this.getMember(group_id, user_id);
      if (member) {
        const roleRef = this.watchRole(group_id, newRole.id);
        Object.assign(roleRef.value, newRole);
        member.role = roleRef;
      }
    }

    clearMembers({ group_id, data }) {
      const members = this.getMembers(group_id);
      if (members && data) {
        for (const uId of data) members.delete(uId);
      }
    }

    delGroupRole({ group_id, role_id, data: newRoleData }) {
      const roleRef = this.getRole(group_id, role_id);
      if (roleRef) {
        const newRoleV = this.watchRole(group_id, newRoleData.id).value;
        Object.assign(newRoleV, newRoleData);
        roleRef.value = newRoleV;
      }
    }

    removeRole(groupId, roleId) {
      try {
        this.getRoles(groupId).delete(roleId);
      } catch (error) {}
    }

    // method to remove group-event
    rmGroupEvent(id, event, cb) {
      try {
        /** @type {Map} */
        const events = this.getGroupEvents(id);
        /** @type {Set} */
        const listeners = events.get(event);
        listeners.delete(cb);
        if (!listeners.size) {
          events.delete(event);
        }
      } catch (error) {
        return;
      }
    }

    rmGroupWS(id) {
      this.groupWS.delete(id);
    }

    connectGroup(group_id, newMsgCB, updateMsgCB, deleteMsgCB) {
      this.sendGroupEvent({ event: "connect", group_id });
      this.onGroup(group_id, "new_msg", newMsgCB);
      this.onGroup(group_id, "edit_msg", updateMsgCB);
      this.onGroup(group_id, "del_msg", deleteMsgCB);
    }

    disconnectGroup(group_id) {
      this.sendGroupEvent({ event: "disconnect", group_id });
      this.rmGroupWS(group_id);
    }

    sendGroupEvent({ event, group_id, ...options }) {
      this.sendEvent({
        event_type: "group",
        event,
        group_id,
        ...options,
      });
    }
  };

const ChatWSMixin = (Cls = Object) =>
  class extends Cls {
    constructor() {
      super();
      // chat event listeners
      this.chatEvents = new Map();
    }

    /**
     * Chat related events handler.
     */
    chatMessage(event, data) {
      this.callEventHandler(this.chatEvents, event, data);
    }

    /**
     * Adds listener for chat related events
     * with given event.
     */
    onChat(event, callback) {
      this.setListener(this.chatEvents, event, callback);
    }

    // method to remove chat event CB
    removeChatEvent(event) {
      this.removeEvent(this.chatEvents, event);
    }

    connectChat(chat_id, newMsgCB, updateMsgCB, deleteMsgCB) {
      this.sendChatEvent({ event: "connect", chat_id });
      this.onChat(`${chat_id}:new`, newMsgCB);
      this.onChat(`${chat_id}:update`, updateMsgCB);
      this.onChat(`${chat_id}:delete`, deleteMsgCB);
    }

    disconnectChat(chat_id) {
      this.sendChatEvent({ event: "disconnect", chat_id });
      this.removeChatEvent(`${chat_id}:new`);
      this.removeChatEvent(`${chat_id}:update`);
      this.removeChatEvent(`${chat_id}:delete`);
    }

    // Base method to send chat messages
    sendChatMsg(chat_id, data) {
      this.sendChatEvent({ event: "send", chat_id, data });
    }

    sendChatEvent({ event, ...options }) {
      this.sendEvent({ event_type: "chat", event, ...options });
    }
  };

const UserWSMixin = (Cls = Object) =>
  class extends Cls {
    constructor() {
      super();
      // User event listeners
      this.userWSUpdate = false;
      this.userEvents = new Map();
      this.trackingPeople = new Map();
      this.userTrackEvents = new Set(["profile_edited", "joint", "left"]);
      this.onUser("profile_edited", this.updateProfile);
      this.onUser("joint", this.userJoint);
      this.onUser("left", this.userLeft);
    }

    hasUser(user_id) {
      return this.trackingPeople.has(user_id);
    }

    getUser(user_id) {
      try {
        return this.trackingPeople.get(user_id).target.value;
      } catch (error) {}
    }

    getTrackUser(user_id) {
      try {
        return this.trackingPeople.get(user_id);
      } catch (error) {}
    }

    /**
     * User related events handler.
     */
    userMessage(event, data) {
      if (this.userTrackEvents.has(event)) {
        data = this.userTrackHandler(data);
      }
      this.callEventHandler(this.userEvents, event, data);
    }

    userTrackHandler({ user_id, data }) {
      if (this.sessionID == user_id) {
        this.userWSUpdate = true;
      }
      const user = this.getUser(user_id);
      data = { user, data };
      return data;
    }

    /**
     * Adds listener for user related events
     * with given event.
     */
    onUser(event, callback) {
      this.setListener(this.userEvents, event, callback);
    }

    /**
     * Called to track events of a user.
     * @param {Any} user_id - user to track.
     */
    watchUser(user_id) {
      if (!user_id) return;
      let tUser = this.getTrackUser(user_id);
      let user = tUser?.target?.value;
      if (!tUser) {
        user = reactive({ id: user_id });
        tUser = { target: ref(user), refCnt: 0 };
        this.sendUserEvent({
          event: "watch",
          user_id,
        });
        this.trackingPeople.set(user_id, tUser);
      }
      ++tUser.refCnt;
      return user;
    }

    refreshUser(user) {
      let wsUser = this.getUser(user?.id);
      wsUser && Object.assign(wsUser, user);
    }

    /**
     * Called to top tracking events of a user.
     * @param {Any} user_id - user to untrack.
     */
    leaveUser(user_id) {
      const tUser = this.getTrackUser(user_id);
      if (!tUser || --tUser.refCnt >= 1) return;
      this.sendUserEvent({
        event: "leave",
        user_id,
      });
      this.trackingPeople.delete(user_id);
    }

    updateProfile({ user, data }) {
      Object.assign(user, data);
    }

    userJoint({ user }) {
      user.status = 1;
    }

    userLeft({ user }) {
      user.status = 0;
    }

    sendUserEvent({ event, ...options }) {
      this.sendEvent({ event_type: "user", event, ...options });
    }

    removeUserEvent(event) {
      this.removeEvent(this.userEvents, event);
    }
  };

/**
 * Class that handles communication between server and session using
 * WS(WebSocket) protocol
 */
class SessionSocket extends UserWSMixin(ChatWSMixin(GroupWSMixin())) {
  // endpoint to connect to
  endpoint = "ws://localhost:6969/ws/session/";

  /**
   * Initializes SessionSocket instance.
   * @param {String} token - User token. Used to connect to server
   */
  constructor(token, sessionID) {
    super();
    // WebSocket object
    this._socket = new WebSocket(`${this.endpoint}?token=${token}`);
    this.sessionID = sessionID;
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
   * Calls message event handler based on event type
   */
  onMessage({ event_type, event, data }, wsEvent) {
    try {
      // console.log(`${event_type}(${event}) =>`, data);
      this[`${event_type}Message`](event, data, wsEvent);
    } catch (error) {
      console.log(error);
    }
  }

  setListener(dict, key, value) {
    value && dict.set(key, value);
  }

  /**
   * Base method to call listeners of an event from dict.
   */
  callEventHandler(dict, event, data) {
    try {
      dict.get(event)(data);
    } catch (error) {
      console.log(error);
    }
  }

  /**
   * Base method to remove an event from events mapping
   */
  removeEvent(dict, event) {
    dict.delete(event);
  }

  /**
   * Base method to send messages to server
   */
  send(data) {
    this._socket.send(JSON.stringify(data));
  }

  sendEvent({ event_type, event, ...options }) {
    if (event_type) {
      this.send({ event_type, event, ...options });
    }
  }

  /**
   * called to close connection with server
   */
  close(code) {
    this._socket.close(code);
  }
}

const defaultStates = {
  // token to get access to server
  access: "",
  // refresh token to update the access token
  refresh: "",
  // Session user object
  user: undefined,
  // session socket object
  socket: null,
  fetching: new Map(),
};

// session store that contains all session info such as
// token, user, socket, etc.
// Controls interaction with server.
export const useSessionStore = defineStore("session", {
  state: () => ({ ...defaultStates }),

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
        // await new Promise((r) => setTimeout(r, 2200));
        return await promise;
      } finally {
        elm.classList.remove(cls);
      }
    },

    /**
     * Patches given fields of a user to server.
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
        const code = err?.response?.data?.code || "";
        if (code.search(/token/i) != -1) {
          const isUpdated = await this.updateToken();
          if (isUpdated) {
            return await this.request(config);
          }
        } else if (code === "user_not_found") {
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
      config.method = "get";
      return this.request(config);
    },

    options(url, config) {
      (config || (config = {})).url = url;
      config.method = "options";
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

    async download(url, name) {
      const { data } = await this.get(url, {
        responseType: "blob",
        baseUrl: "",
      });
      const href = URL.createObjectURL(data);
      const link = document.createElement("a");
      link.style.display = "none";
      link.href = href;
      link.setAttribute("download", name);
      link.click();

      URL.revokeObjectURL(href);
    },

    async fetchUser(userId) {
      return (await this.get(`users/${userId}/`)).data;
    },

    /**
     * Fetches session user data from the server
     */
    async fetchSession() {
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
      if (!(this.access || this.refresh)) return;
      try {
        await this.fetchSession();
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
      await this.animate(this.fetchSession());
    },

    _resetStore() {
      Object.assign(this, defaultStates);
    },

    /**
     * Base method to logout user.
     */
    logout() {
      this.socket?.close();
      this.socket = null;
      this.user = null;
      localStorage.clear();
      this._resetStore();
    },

    /**
     * Connects to the server using WebSocket protocol.
     */
    connectServer(callback) {
      this.socket = markRaw(new SessionSocket(this.access, this.user.id));
      this.socket.onWS("open", callback);
    },

    refreshUser(user) {
      const { id } = user;
      const key = `user:${id}`;
      let prom = this.fetching.get(key);
      if (prom) return prom;
      prom = this.fetchUser(id).then((data) => {
        Object.assign(user, data);
        this.fetching.delete(key);
        return data;
      });
      this.fetching.set(key, prom);
    },

    refreshRole(group, role) {
      const { id } = role;
      const key = `group(${group.id}):role(${id})`;
      let prom = this.fetching.get(key);
      if (prom) return prom;
      prom = this.get(`${group.url}roles/${id}`).then(({ data }) => {
        Object.assign(role, data, { fetched: true });
        this.fetching.delete(key);
        return data;
      });
      return prom;
    },

    getWSUser(id, fetch = false) {
      let user = this.socket.watchUser(id);
      if (fetch && Object.keys(user).length == 1) {
        this.refreshUser(user);
      }
      return user;
    },

    async getWSRole(group, roleId) {
      const roleRef = this.socket.watchRole(group.id, roleId);
      const role = roleRef.value;
      if (!role.fetched) {
        await this.refreshRole(group, role);
      }
      return roleRef;
    },
  },
});

const sessionStore = useSessionStore();

// tracks changes of session store if access or refresh has
// changed it'll be updated in local storage too.
sessionStore.$subscribe((mutation, state) => {
  if (!state) return;
  const { access, refresh } = state;
  access && localStorage.setItem("access", state.access);
  refresh && localStorage.setItem("refresh", state.refresh);
});
