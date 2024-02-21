<template>
  <div class="member-box" @click="$profile.show(user.id)">
    <UserAvatar :user="user" class="w-14" />
    <div class="overflow-hidden truncate">
      <h6 class="member-name">{{ full_name }}</h6>
      <p class="member-role">
        <span v-if="role.is_owner" class="owner-role text-secondary">
          <i class="fa-solid fa-user-astronaut"></i>
        </span>
        <span v-else-if="role.super_admin" class="text-accent">
          <i class="fa-solid fa-user-tie"></i>
        </span>
        {{ role.name }}
      </p>
    </div>
  </div>
</template>

<script>
import UserAvatar from "@/components/User/UserAvatar.vue";
import trackUser from "@/components/User/trackUser.js";
import trackMember from "./trackMember.js";

export default {
  props: {
    member: {
      type: Object,
      required: true,
    },
    group: {
      type: Object,
      required: true,
    },
  },

  computed: {
    user() {
      return this.member.user;
    },

    role() {
      return this.member.role;
    },

    full_name() {
      return `${this.user.first_name} ${this.user.last_name}`;
    },
  },

  created() {
    this.$session.socket.refreshUser(this.user);
  },

  components: { UserAvatar },
  mixins: [trackUser, trackMember],
  watch: {
    member(a, b) {
      if (a != b) {
        Object.assign(this.member.role, this.wsRole);
      }
    },
  },
};
</script>

<style scoped>
.member-box {
  @apply flex gap-3 p-2 px-2.5 
  transition-transform bg-base-content/5 rounded-2xl 
  cursor-pointer hover:bg-base-content/15;
}

.member-box:active {
  @apply scale-[0.97];
}

.member-name {
  @apply text-base-content/90;
}

.member-role {
  @apply text-base-content/80;
}
</style>
