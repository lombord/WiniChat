import DynamicComp from "@/components/Utils/DynamicComp.vue";

export default {
  props: {
    chat: {
      type: Object,
      required: true,
    },
  },

  _chatComponents: {},
  _compPaths: {},

  computed: {
    chatType() {
      return this.chat.type;
    },

    getKey() {
      return this.$chats.getChatKey;
    },

    currComponent() {
      return this.$options._chatComponents[this.chatType];
    },
    currPath() {
      return this.$options._compPaths[this.chatType];
    },
  },

  components: { DynamicComp },
};
