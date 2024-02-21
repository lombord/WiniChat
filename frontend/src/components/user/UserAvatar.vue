<template>
  <div class="avatar" :class="avatarCls">
    <div class="round-img img-wrapper" v-bind="$attrs">
      <ImgAnim :src="user.photo" />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    user: {
      type: Object,
      required: true,
    },
  },
  computed: {
    avatarCls() {
      return this.user.status ? "online" : "offline";
    },
  },
};
</script>

<style scoped>
.img-wrapper {
  @apply w-16 aspect-square;
}
</style>
