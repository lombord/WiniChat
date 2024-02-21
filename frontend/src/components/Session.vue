<template>
  <div v-if="loaded">
    <RouterView />
  </div>
</template>

<script>
export default {
  data: () => ({
    loaded: false,
    oldUser: null,
    wsUser: null,
  }),

  created() {
    const { classList } = document.body;
    classList.add("load-anim");
    this.$session.connectServer(() => {
      classList.remove("load-anim");
      this.loaded = true;
      this.wsUser = this.$session.getWSUser(this.user.id);
      this.socket.refreshUser(this.user);
    });
    window.addEventListener(
      "beforeunload",
      () => {
        this?.$session?.socket.close();
      },
      { once: true }
    );

    this.oldUser = { ...this.user };
  },

  beforeUnmount() {
    this.socket?.leaveUser(this.user?.id);
  },

  computed: {
    user() {
      return this.$session.user;
    },
    socket() {
      return this.$session.socket;
    },
  },

  watch: {
    user: {
      handler(user) {
        if (this.socket.userWSUpdate) {
          this.socket.userWSUpdate = false;
          return;
        }
        let changes = Object.entries(user).filter(
          ([key, val]) => this.oldUser[key] != val
        );
        if (!changes.length) return;
        this.oldUser = { ...user };
        changes = Object.fromEntries(changes);
        Object.assign(this.wsUser, changes);
        const data = {
          event: "edit",
          data: changes,
        };
        this.$session.socket.sendUserEvent(data);
      },
      deep: true,
    },
    wsUser: {
      handler(value) {
        Object.assign(this.user, value);
      },
      deep: true,
    },
  },
};
</script>

<style scoped></style>
