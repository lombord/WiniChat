<template>
  <div class="ban-box" @click="$profile.show(user.id)">
    <UserAvatar :user="user" class="w-[60px]" />
    <div class="flex-1">
      <h6 class="text-base-content/90">{{ fullName }}</h6>
      <p class="font-bold flex items-center gap-2 text-base-content/80">
        <span>Banned by</span>
        <span @click.stop="$profile.show(bannedBy.id)" class="banned-by">
          {{ bannedBy.username }}</span
        >
      </p>
    </div>
  </div>
</template>

<script>
import UserAvatar from "@/components/User/UserAvatar.vue";
import trackUser from "@/components/User/trackUser.js";

export default {
  props: {
    ban: {
      type: Object,
      required: true,
    },
  },

  computed: {
    user() {
      return this.ban.user;
    },

    userId() {
      return this.user.id;
    },

    bannedBy() {
      return this.ban.banned_by;
    },

    fullName() {
      const { user } = this.ban;
      return `${user.first_name} ${user.last_name}`;
    },
    username() {
      return this.user.username;
    },
  },

  mixins: [trackUser],

  components: { UserAvatar },
};
</script>

<style scoped>
.ban-box {
  @apply flex gap-3 items-center 
  p-2 rounded-2xl bg-base-200
  hover:bg-base-content/10
  transition-transform
  cursor-pointer;
  transform: translate3d(0, 0, 0);
  backface-visibility: hidden;
}

.ban-box:not(:has(.banned-by:active)):active {
  transform: scale(0.97) translate3D(0, 0, 0);
}

.banned-by {
  @apply text-primary-light hover:text-primary-medium active:scale-95 transition
   hover:underline;
}
</style>
