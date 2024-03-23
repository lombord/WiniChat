import { v4 as uuid4 } from "uuid";

import { reactive } from "vue";
import moment from "moment";

import fetchData from "@/mixins/fetchData.js";

import Messages from "@/components/ChatCommon/Messages.vue";
import ChatInput from "@/components/ChatCommon/ChatInput";
import ScrollBottom from "@/components/ChatCommon/ScrollBottom.vue";

export default {
  data: () => ({
    // scroll related properties
    showScroll: false,
    scrollTop: 0,
    // message related properties
    message: null,
    editing: null,
    currProm: null,
    contexts: {},

    // fetch properties
    reverseFetch: true,
    limit: 30,
  }),

  props: {
    chat: {
      type: Object,
      required: true,
    },
    scrollElm: {
      type: Element,
      required: true,
    },
  },

  computed: {
    user() {
      return this.$session.user;
    },

    socket() {
      return this.$session.socket;
    },

    url() {
      return this.chat.url;
    },

    fetchUrl() {
      return `${this.url}messages/`;
    },

    msgUrl() {
      return this.fetchUrl;
    },

    isFullScroll() {
      const diff =
        this.scrollElm.scrollHeight -
        this.scrollTop -
        this.scrollElm.clientHeight;
      return diff <= 20;
    },

    commonContext() {
      return {
        copy: {
          label: "Copy",
          icon: "fa-regular fa-clone",
          cb: this.copyMsg,
        },
        edit: {
          label: "Edit",
          icon: "fa-solid fa-pen",
          cb: this.editMsg,
        },
        delete: {
          label: "Delete",
          icon: "fa-solid fa-trash",
          cls: "text-error",
          cb: this.deleteMsg,
        },
      };
    },

    dateFMT() {
      return "YYYY-MM-DD";
    },

    messages() {
      const result = Array.from(this.dataList.entries());
      result.sort(([k1], [k2]) => (moment(k1) > moment(k2) ? -1 : 1));
      return result;
    },
  },

  created() {
    this.resetMsg();
  },

  mounted() {
    this.scrollTop = this.scrollElm.scrollTop;
    this.scrollElm.addEventListener("scroll", this.scrolled);
  },

  async activated() {
    await this.$nextTick();
    this.scrollTo(this.scrollTop);
    this.scrollElm.addEventListener("scroll", this.scrolled);
  },

  deactivated() {
    this.scrollElm.removeEventListener("scroll", this.scrolled);
  },

  unmounted() {
    this.scrollElm.removeEventListener("scroll", this.scrolled);
  },

  methods: {
    pushOrShift(msg, action = "push") {
      const isPush = action == "push";
      const messages = this.dataList;
      const created = moment(msg.created).format(this.dateFMT);
      let contexts = messages.get(created);
      if (!contexts) {
        contexts = [];
        messages.set(created, contexts);
      }
      let context = contexts[isPush ? contexts.length - 1 : 0];
      if (!context || context.owner.id != msg.owner) {
        context = {
          owner: { id: msg.owner },
          messages: [],
          uuid: `context:${uuid4()}`,
        };
        contexts[action](context);
      }
      context.messages[action](msg);
      if (msg.id) {
        this.contexts[msg.id] = context.messages;
      }
      return context.messages;
    },

    pushMsg(msg) {
      return this.pushOrShift(msg);
    },

    unshiftMsg(msg) {
      return this.pushOrShift(msg, "unshift");
    },

    firstAdd(data) {
      this.dataList = new Map();
      this.addNext(data);
    },

    addNext(messages) {
      messages.forEach(this.pushMsg);
    },

    addPrevious(messages) {
      if (!(messages && messages.length)) return;
      for (let i = messages.length - 1; i >= 0; i--) {
        this.unshiftMsg(messages[i]);
      }
    },

    getContextMenu(user) {
      if (user.id == this.user.id) {
        return this.getSessionContext();
      }
      return this.getContextFor(user);
    },

    getSessionContext() {
      return Object.values(this.commonContext);
    },

    getContextFor(user) {
      return [this.commonContext.copy];
    },

    async postMsg(tmpFiles) {
      const msg = this.message;
      if (!(msg.content || msg.files.length)) return;
      const [msgItem, context] = await this.addMsg(
        this.makeTmpMsg(msg.content, tmpFiles),
        true
      );
      this.resetMsg();
      this.currProm = this.submitMsg(msg).then((data) => {
        Object.assign(msgItem, data);
        this.chat.latest = msgItem;
        this.contexts[data.id] = context;
        if (tmpFiles) {
          tmpFiles.forEach(({ url }) => URL.revokeObjectURL(url));
        }
        this.messagePosted(data);
      });
    },

    async submitMsg(msg) {
      if (this.currProm) await this.currProm;
      const data = this.toFormData(msg);
      try {
        const prom = this.$session.post(this.msgUrl, data, { timeout: 36e5 });
        return (await this.$session.animate(prom, null, "xyz")).data;
      } catch (error) {
        this.$flashes.axiosError(error);
      }
    },

    async addMsg(msg, scroll = false) {
      if (this.previous) return;
      this.next && this.nextOff++;
      msg = reactive(msg);
      const context = this.unshiftMsg(msg);
      if (scroll || this.isFullScroll) {
        await this.$nextTick();
        requestAnimationFrame(this.scrollBottom);
      }
      return [msg, context];
    },

    /**
     * Hook called after message has been posted
     */
    messagePosted(data) {
      return;
    },

    async copyMsg(msg) {
      await navigator.clipboard.writeText(msg.content);
    },

    resetMsg() {
      this.message = {
        content: "",
        files: [],
      };
    },

    makeTmpMsg(content, files) {
      const result = {
        uuid: uuid4(),
        content,
        files,
        created: new Date().toJSON(),
        owner: this.user.id,
      };
      return result;
    },

    toFormData(msg) {
      const form = new FormData();
      form.append("content", msg.content);
      for (let i = 0; i < msg.files.length; i++) {
        form.append("files", msg.files[i]);
      }
      return form;
    },

    // Hook called after message has been patched
    msgPatched(msg, data, rData) {
      return;
    },

    async patchMessage(msg, data) {
      try {
        const { data: rData } = await this.$session.patch(msg.url, data);
        this.msgPatched(msg, data, rData);
        return rData;
      } catch (error) {
        this.$flashes.axiosError(error);
      }
    },

    // Hook called after message has been deleted
    msgDeleted(msg) {
      return;
    },

    async deleteMsg(msg) {
      try {
        await this.$session.delete(msg.url);
        this.removeMsg(msg.id);
        this.msgDeleted(msg);
      } catch (error) {
        this.$flashes.axiosError(error);
      }
    },

    cancelEdit() {
      this.editing = null;
      this.resetMsg();
    },

    async editMsg(msg) {
      this.resetMsg();
      await this.$nextTick();
      this.editing = msg;
      this.message = { ...msg };
    },

    async saveEdit() {
      const { content } = this.message;
      const data = { content, is_edited: true };
      await this.patchMessage(this.editing, data);
      Object.assign(this.editing, data);
      this.cancelEdit();
    },

    // Hook called before the message being updated
    // beforeUpdate(data, msg, idx) {
    //   return;
    // },

    findMsgIdx(id) {
      const context = this.contexts[id];
      if (!context) return [];
      const idx = context.findIndex((msg) => msg.id == id);
      return [context, idx];
    },

    findMsg(id) {
      const context = this.contexts[id];
      if (!context) return;
      return context.find((msg) => msg.id == id);
    },

    updateMsg({ msg_id, data }) {
      const msg = this.findMsg(msg_id);
      msg && Object.assign(msg, data);
    },

    removeMsg(id) {
      const [context, idx] = this.findMsgIdx(id);
      if (context && idx >= 0) {
        if (this.next && this.nextOff > 0) {
          this.nextOff--;
        }
        delete this.contexts[id];
        const [msg] = context.splice(idx, 1);
        if (!msg.seen && msg.owner != this.user.id) {
          this.chat.unread = Math.max(this.chat.unread - 1, 0);
        }
      }
    },

    scrollBottom(options) {
      requestAnimationFrame(() =>
        this.scrollElm.scrollTo({
          top: this.scrollElm.scrollHeight,
          ...options,
        })
      );
    },

    scrollTo(height) {
      requestAnimationFrame(() => this.scrollElm.scrollTo({ top: height }));
    },

    scrolled({ target: el }) {
      this.scrollTop = el.scrollTop;
      this.showScroll = !(
        Math.abs(el.scrollHeight - el.scrollTop - el.clientHeight) < 150
      );
    },
  },

  mixins: [fetchData],
  components: { Messages, ScrollBottom, ChatInput },
};
