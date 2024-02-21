export default {
  data: () => ({
    wsUser: null,
    wsFetch: false,
  }),

  created() {
    this.wsUser = this.$session.getWSUser(this.userId, this.wsFetch);
  },

  beforeUnmount() {
    this.$session.socket.leaveUser(this.userId);
  },

  watch: {
    wsUser: {
      handler(value) {
        Object.assign(this.user, value);
      },
      deep: true,
    },
  },
};
