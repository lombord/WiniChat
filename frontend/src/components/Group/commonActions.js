export default {
  methods: {
    async leaveGroup() {
      const session = this.$session;
      const { group } = this;
      try {
        await session.delete(`${group.url}leave/`);
        session.socket.sendGroupEvent({
          event: "leave",
          group_id: group.id,
          user_id: session.user.id,
        });
        this.$chats.removeChat(group);
      } catch (error) {
        this.$flashes.axiosError(error);
      }
    },
  },
};
