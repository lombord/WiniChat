<template>
  <div></div>
</template>

<script>
export default {
  async beforeMount() {
    if (this.$session.isAuthenticated) {
      this.$session.logout();
      await this.$router.push({ name: "login" });
      this.$flashes.info("You have been logged out.");
    }
  },
};
</script>

<style scoped></style>
