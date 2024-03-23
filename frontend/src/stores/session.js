// Store that controls communication with server
// using `http(s)` and `ws` protocols

import { ref, reactive, markRaw, shallowReadonly } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { request } from "@/plugins/request.js";

const GroupWSMixin = (Cls = Object) =>
  /**
   * Mixin to handle Group WS Events
   */

  class extends Cls {
    constructor() {
      super();

      // map of group websocket objects
      this.groupWS = new Map();
      // map of general group websocket event handlers
      this.grpGenEvents = new Map();
      this.onGroupGen("role_updated", ({ group_id, role_id, data }) =>
        this.refreshRole(group_id, role_id, data)
      );
      this.onGroupGen("del_role", this.delGroupRole.bind(this));
      this.onGroupGen("remove_members", this.clearMembers.bind(this));
      this.onGroupGen("change_role", this.changeMemberRole.bind(this));
    }

    /**
     * SetsUp group ws object for given group id
     * @param {Number} id - Group id
     * @return {Object} Returns GroupWS object.
     */
    setUpGroupWS(id) {
      const wsObj = { events: new Map(), roles: new Map(), members: new Map() };
      this.groupWS.set(id, wsObj);
      return wsObj;
    }

    /**
     * Returns GroupWS object prop of given group.
     * @param {Number} id - Group id
     * @param {String} prop - Property name
     */
    getGroupWS(id, prop) {
      try {
        return this.groupWS.get(id)[prop];
      } catch (error) {}
    }

    /**
     * Tries to get GroupWS object if it exists,
     * otherwise creates it based on id and returns prop
     * @param {Number} id - Group id
     * @param {String} prop - Property name
     */
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

    /**
     * Returns Set of group listeners for given event
     * @param {Number} id - Group id
     * @param {String} event - Event name
     * @return {Set} Brief description of the returning value here.
     */
    getEventListeners(id, event) {
      try {
        return this.groupWS.get(id).events.get(event);
      } catch (error) {}
    }

    /**
     * Group event handler for GroupWS objects.
     * Calls event listeners of an event with received data
     * @param {String} event - Event name
     * @param {Object} data - WS data
     */
    groupEventHandler(event, { group_id, data, ...rest }) {
      const listeners = this.getEventListeners(group_id, event);
      if (!listeners) return;
      for (const callback of listeners) {
        callback(data, rest);
      }
    }

    /**
     * General group events handler
     * @param {String} event - Event name
     * @param {Object} data - ws data
     */
    grpGenHandler(event, data) {
      let callback = this.grpGenEvents.get(event);
      if (callback) {
        callback(data);
      }
    }

    /**
     * Sets general group listener for given event
     * @param {String} event - Event name
     * @param {Function} callback - Callback function
     */
    onGroupGen(event, callback) {
      this.grpGenEvents.set(event, callback);
    }

    /**
     * Sets event listener for given event
     * @param {Number} id - Group id
     * @param {String} event - Event name
     * @param {Function} callback - Callback function
     */
    onGroup(id, event, callback) {
      const events = this.acquireGroupWS(id, "events");
      let listeners = events.get(event);
      if (!listeners) {
        listeners = new Set();
        events.set(event, listeners);
      }
      listeners.add(callback);
    }

    /**
     * Returns events map for given group
     * @param {Number} id - Group id
     * @return {Map} Map of event-listeners
     */
    getGroupEvents(id) {
      return this.getGroupWS(id, "events");
    }

    /**
     * Returns Map of Reactive trackable roles of a group
     * @param {Number} id - Group id
     * @return {Map} Map of reactive role objects
     */
    getRoles(id) {
      return this.getGroupWS(id, "roles");
    }

    /**
     * Returns Map of Reactive trackable members of a group
     * @param {Number} id - Group id
     * @return {Map} Map of reactive member objects
     */
    getMembers(id) {
      return this.getGroupWS(id, "members");
    }

    /**
     * Returns reactive role of a group
     * @param {Number} groupId - Group id
     * @param {Number} roleId - Role id
     * @return {Proxy} reactive role object
     */
    getRole(groupId, roleId) {
      return this.getRoles(groupId)?.get(roleId);
    }

    /**
     * Returns reactive member of a group
     * @param {Number} groupId - Group id
     * @param {Number} userId - User id
     * @return {Proxy} reactive member object
     */
    getMember(groupId, userId) {
      return this.getMembers(groupId)?.get(userId);
    }

    /**
     * Creates reactive role object for a group if it doesn't exist
     * otherwise returns the existing one
     * @param {Number} groupId - Group id
     * @param {Number} roleId - Role id
     * @return {Proxy} reactive role object
     */
    watchRole(groupId, roleId) {
      const roles = this.acquireGroupWS(groupId, "roles");
      let role = roles.get(roleId);
      if (!role) {
        role = ref({ id: roleId });
        roles.set(roleId, role);
      }
      return shallowReadonly(role);
    }

    /**
     * Creates reactive member object for a group if it doesn't exist
     * otherwise returns the existing one
     * @param {Number} groupId - Group id
     * @param {Number} userId - User id
     * @param {Number} roleId - Member role id
     * @return {Proxy} reactive member object
     */
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

    /**
     * Refreshes role of a group with the given data
     * @param {Number} groupId - Group id
     * @param {Number} roleId - Member role id
     * @param {Object} data - Refresh data
     */
    refreshRole(groupId, roleId, data) {
      let role = this.getRole(groupId, roleId);
      if (role && data) {
        Object.assign(role.value, data);
      }
    }

    /**
     * Called to change reactive member's role of a group
     * @param {Number} group_id - Group id
     * @param {Number} user_id - User id
     * @param {Object} data - new role data
     */
    changeMemberRole({ group_id, user_id, data: newRole }) {
      const member = this.getMember(group_id, user_id);
      if (member) {
        const roleRef = this.watchRole(group_id, newRole.id);
        Object.assign(roleRef.value, newRole);
        member.role = roleRef;
      }
    }

    /**
     * Removes list of tracking members from a GroupWS object
     * @param {Number} groupId - Group id
     * @param {Array} data - List of member user ids
     */
    clearMembers({ group_id, data }) {
      const members = this.getMembers(group_id);
      if (members && data) {
        for (const uId of data) members.delete(uId);
      }
    }

    /**
     * Removes and stops tracking role of a group,
     * and replaces it with new one
     * @param {Number} groupId - Group id
     * @param {Number} userId - User id
     * @param {Object} data - New Role object
     */
    delGroupRole({ group_id, role_id, data: newRoleData }) {
      const roleRef = this.getRole(group_id, role_id);
      if (roleRef) {
        const newRoleV = this.watchRole(group_id, newRoleData.id).value;
        Object.assign(newRoleV, newRoleData);
        roleRef.value = newRoleV;
      }
    }

    /**
     * Called to stop tracking role of a group
     * @param {Number} groupId - Group id
     * @param {Number} roleId - role id
     */
    removeRole(groupId, roleId) {
      try {
        this.getRoles(groupId).delete(roleId);
      } catch (error) {}
    }

    /**
     * Removes event from a group
     * @param {Number} id - Group id
     * @param {String} event - User id
     * @param {Number} roleId - Member role id
     * @return {Proxy} reactive member object
     */
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

    /**
     * Removes GroupWS object from group ws map
     * @param {Number} id - Group id
     */
    rmGroupWS(id) {
      this.groupWS.delete(id);
    }

    /**
     * Connects session to group channel layer to track
     * Group WS events
     * @param {Number} groupId - Group id
     * @param {Function} newMsgCB - New message callback
     * @param {Function} updateMsgCB - Update message callback
     * @param {Function} deleteMsgCB - Delete message callback
     */
    connectGroup(group_id, newMsgCB, updateMsgCB, deleteMsgCB) {
      this.sendGroupEvent({ event: "connect", group_id });
      this.onGroup(group_id, "new_msg", newMsgCB);
      this.onGroup(group_id, "edit_msg", updateMsgCB);
      this.onGroup(group_id, "del_msg", deleteMsgCB);
    }

    /**
     * Disconnects from group layer and deletes GroupWS object
     * @param {Number} groupId - Group id
     */
    disconnectGroup(group_id) {
      this.sendGroupEvent({ event: "disconnect", group_id });
      this.rmGroupWS(group_id);
    }

    /**
     * Base method to send group events
     * @param {String} event - event name
     * @param {Number} group_id - Group id
     * @param {Object} options - extra data
     */
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
  /**
   * Mixin to handle Private Chat WS events
   */

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
  /**
   * Mixin to handle User related WS events
   */

  class extends Cls {
    constructor() {
      super();
      this.userWSUpdate = false;
      // User event listeners
      this.userEvents = new Map();
      // Map of tracking people
      this.trackingPeople = new Map();
      // Base Events for tracking people
      this.userTrackEvents = new Set(["profile_edited", "joint", "left"]);
      this.onUser("profile_edited", this.updateProfile);
      this.onUser("joint", this.userJoint);
      this.onUser("left", this.userLeft);
    }

    /**
     * Returns whether user is being tracked
     * @param {Number} user_id - User id
     * @return {Boolean}
     */
    hasUser(user_id) {
      return this.trackingPeople.has(user_id);
    }

    /**
     * Returns trackable reactive user object if
     * @param {Number} user_id - User id
     * @return {[Proxy, undefined]} reactive user object
     */
    getUser(user_id) {
      try {
        return this.trackingPeople.get(user_id).target.value;
      } catch (error) {}
    }

    /**
     * Returns track user object
     * @param {Number} user_id - User id
     * @return {[Proxy, undefined]} reference to track object
     */
    getTrackUser(user_id) {
      try {
        return this.trackingPeople.get(user_id);
      } catch (error) {}
    }

    /**
     * User related message event handler.
     * Calls listeners of an event
     * @param {String} event - Event name
     * @param {Object} data - WS object
     */
    userMessage(event, data) {
      if (this.userTrackEvents.has(event)) {
        data = this.userTrackHandler(data);
      }
      this.callEventHandler(this.userEvents, event, data);
    }

    /**
     * User track related events data wrapper
     * @param {Number} user_id - User id
     * @param {Object} data - user WS data
     * @return {Object} wrapped data
     */
    userTrackHandler({ user_id, data }) {
      if (this.sessionId == user_id) {
        this.userWSUpdate = true;
      }
      const user = this.getUser(user_id);
      data = { user, data };
      return data;
    }

    /**
     * Sets listener for given event
     * @param {String} event - Event name
     * @param {Function} callback - callback function
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
     * Called to stop tracking events of a user.
     * @param {Any} user_id - user id.
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

    /**
     * Base user ws event sender
     * @param {String} event - Event name
     * @param {Object} options - extra data
     */
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
  /**
   * Base session socket class that inherits from
   * all ws event handler classes
   */

  // ws route endpoint

  get endpoint() {
    let protocol = "ws";
    if (location.protocol == "https:") {
      protocol = "wss";
    }
    return `${protocol}://${location.host}/django-ws/session/`;
  }

  /**
   * Initializes SessionSocket instance.
   * @param {String} token - User token. Used to connect to server
   */
  constructor(token, sessionId) {
    super();

    // WebSocket object
    this._socket = new WebSocket(`${this.endpoint}?token=${token}`);
    // current session user id
    this.sessionId = sessionId;
    // on message call base message handler method
    this.onWS("message", (...args) => this.onMessage(...args));
  }

  /**
   * Base method to set ws event listeners.
   * @param {String} type - ws event name.
   * @param {Function} callback - callback function.
   * @param {Object} options - extra options.
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
   * Base ws message event handler.
   * Calls base message event handler based on event type
   */
  onMessage({ event_type, event, data }, wsEvent) {
    try {
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
   * Base method to remove an event from mapping
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

  /**
   * Base ws event sender to the server
   * @param {String} event_type - Type of event
   * @param {String} event - Event name
   * @param {Object} options - extra data to send
   */
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
    // indicates whether session is authenticated
    isAuthenticated: (state) => {
      return !!state.user;
    },
    // indicates whether session is loaded
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
     * Animates promise with given elm and class.
     * @param {Promise} promise - promise to wrap
     * @param {HTMLElement} elm - elm to animate
     * @param {String} class - css selector.
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
     * Base request method to send token related requests.
     *
     * If any error occurs during request and it is related with token
     * it will try to refresh token
     *
     * if it doesn't work user will be logged out,
     * otherwise request will be sent again
     * @param {Object} config - axios request config.
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
     * Sends get request.
     * @param {String} url - endpoint URL
     * @param {Object} config - extra axios config
     * @return {Promise} Request promise.
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
     * Sends delete request.
     * @param {String} url - endpoint URL
     * @param {Object} config - extra axios config
     * @return {Promise} Request promise.
     */
    delete(url, config) {
      (config || (config = {})).url = url;
      config.method = "delete";
      return this.request(config);
    },

    /**
     * Base method for requests with body (post, put, patch, etc.).
     * @param {String} method - method name
     * @param {String} url - endpoint URL
     * @param {Object} config - axios config
     * @return {Promise} - Request promise.
     */
    dataRequest(method, url, data, config) {
      const _new = { url, data, method };
      return this.request(this.update(config, _new));
    },

    /**
     * Method to send post request wraps 'dataRequest' function
     * @return {Promise} Returns promise.
     */
    post(...args) {
      return this.dataRequest("post", ...args);
    },

    /**
     * Method to send put request wraps 'dataRequest' function
     * @return {Promise} Returns promise.
     */
    put(...args) {
      return this.dataRequest("put", ...args);
    },

    /**
     * Method to send patch request wraps 'dataRequest' function
     * @return {Promise} Returns promise.
     */
    patch(...args) {
      return this.dataRequest("patch", ...args);
    },

    /**
     * Sends blob request and downloads file if request succeeds.
     * @param {String} url - endpoint URL
     * @param {String} name - file name to download as
     * @return {Promise} Request promise.
     */
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

    /**
     * Base method to fetch user infos
     * @param {Number} userId - User id
     * @param {String} name - file name to download as
     * @return {Promise} Request promise.
     */
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

    /**
     * Refreshes given track user object
     * @param {Object} user - tracking user object
     * @return {Promise} Request promise.
     */
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

    /**
     * Refreshes given track role object of a group
     * @param {Object} group - Role Group
     * @param {Object} role - tracking role object
     * @return {Promise} Request promise.
     */
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
