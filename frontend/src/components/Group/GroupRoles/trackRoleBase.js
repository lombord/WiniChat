export default {
  computed: {
    socket() {
      return this.$session.socket;
    },

    trackRole() {
      return this.role;
    },

    groupId() {
      return this.group.id;
    },
  },

  methods: {
    refreshWSRole(data) {
      if (this.wsRole) {
        Object.assign(this.wsRole, data);
      } else {
        this.socket.refreshRole(this.groupId, this.trackRole.id, data);
      }
    },
  },

  watch: {
    wsRole: {
      handler(value) {
        try {
          Object.assign(this.trackRole, value);
        } catch (error) {
          console.log(error);
        }
      },
      deep: true,
    },
  },
};
