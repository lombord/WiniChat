export default {
  data: () => ({
    members: null,
  }),

  props: {
    group: {
      type: Object,
      required: true,
    },
  },

  computed: {
    fetchUrl() {
      return `${this.group.url}members/`;
    },

    sortedMembers() {
      const members = Array.from(this.members.values());
      members.sort((m1, m2) => {
        const [a, b] = [new Date(m1.last_activity), new Date(m2.last_activity)];
        return a >= b ? -1 : 1;
      });
      return members;
    },

    socket() {
      return this.$session.socket;
    },
  },

  created() {
    const {
      socket,
      group: { id },
    } = this;
    socket.onGroup(id, "new_members", this.addWSMembers);
    socket.onGroup(id, "remove_members", this.removeMembers);
  },

  beforeUnmount() {
    const {
      socket,
      group: { id },
    } = this;
    socket.rmGroupEvent(id, "new_members", this.addWSMembers);
    socket.rmGroupEvent(id, "remove_members", this.removeMembers);
  },

  methods: {
    initMembers(data) {
      const members = (this.members = new Map());
      this.addMembers(data);
      return members;
    },

    addWSMembers(data) {
      this.addMembers(data);
    },

    addMembers(members) {
      members.forEach(this.addMember);
    },

    addMember(member) {
      this.members.set(member.user.id, member);
    },

    removeMembers(users) {
      users.forEach(this.removeMember);
    },

    removeMember(userId) {
      this.members.delete(userId);
    },
  },
};
