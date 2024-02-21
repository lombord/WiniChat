import trackRoleBase from "./trackRoleBase.js";

export default {
  data: () => ({
    wsRole: null,
  }),

  created() {
    this.setUpWSRole();
  },

  methods: {
    setUpWSRole() {
      try {
        this.wsRole = this.socket.watchRole(this.groupId, this.trackRole.id);
      } catch (error) {}
    },
  },

  mixins: [trackRoleBase],
};
