// Mixin to login a user
export default {
  methods: {
    async login(data) {
      const promise = this.$session.login(data);
      try {
        await this.$session.animate(promise, this.$refs.loginBox);
        await this.$router.push({ name: "home" });
        const msg = `You have logged as ${this.$session.user.username}`;
        this.$flashes.info(msg);
      } catch (err) {
        this.$flashes.error("Login or password is wrong!");
      }
    },
  },
};
