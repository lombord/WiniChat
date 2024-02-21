export default {
  props: {
    isSession: {
      type: Boolean,
      default: true,
    },
  },

  computed: {
    request() {
      return this.isSession ? this.$session.request : this.$request;
    },
  },
};
