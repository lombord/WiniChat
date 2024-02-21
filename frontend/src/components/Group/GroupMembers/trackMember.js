import trackRoleBase from "../GroupRoles/trackRoleBase.js";

export default {
  data: () => ({
    wsMember: null,
    autoSetUp: true,
  }),

  computed: {
    userId() {
      return this.member.user.id;
    },

    wsRole() {
      return this.wsMember?.role;
    },
  },

  created() {
    if (this.autoSetUp) {
      this.setUpWSMember();
    }
  },

  methods: {
    setUpWSMember() {
      try {
        this.wsMember = this.socket.watchMember(
          this.groupId,
          this.userId,
          this.trackRole.id
        );
      } catch (error) {}
    },
  },

  mixins: [trackRoleBase],
};
