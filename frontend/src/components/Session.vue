<template>
  <div v-if="loaded">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  data: () => ({
    loaded: false,
  }),

  created() {
    const { classList } = document.body;
    classList.add("load-anim");
    this.$session.connectServer(() => {
      classList.remove("load-anim");
      this.loaded = true;
    });
    window.addEventListener(
      "beforeunload",
      () => {
        this.$session.socket.close();
      },
      { once: true }
    );
  },

  watch: {
    "$session.user": {
      handler(user) {
        const data = {
          event: "user_edit",
          data: user,
        };
        this.$session.socket.send(data);
      },
      deep: true,
    },
  },
};
</script>

<style scoped></style>
