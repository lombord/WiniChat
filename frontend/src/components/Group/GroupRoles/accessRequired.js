import permission from "./permission.js";

export default {
  data: () => ({
    accessPerm: null,
  }),

  computed: {
    hasAccess() {
      return this.hasPerm(this.accessPerm);
    },
  },

  methods: {
    checkAccess() {
      if (!this.hasAccess) {
        this.accessDenied();
        this.$emit("accessDenied");
      }
    },

    accessDenied() {
      this.$emit("close");
    },
  },

  watch: {
    hasAccess(val) {
      this.checkAccess();
    },
  },

  emits: ["accessDenied"],
  mixins: [permission],
};
