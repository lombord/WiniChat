<template>
  <div></div>
</template>

<script>
export default {
  beforeMount() {
    this.$session.logout();
    this.$router.push({ name: "login" });
  },
};
</script>

<style scoped></style>
