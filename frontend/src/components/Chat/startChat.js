export default {
  methods: {
    async startChat(to_user) {
      const response = await this.$session.post("chats/", { to_user });
      const { data } = response;
      this.$chats.add(data);
      this.$session.socket.sendChatEvent({
        event: "new",
        chat_id: data.id,
      });
      return response;
    },
  },
};
