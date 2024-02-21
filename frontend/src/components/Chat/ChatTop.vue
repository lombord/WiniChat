<template>
  <div class="user-short" @click="$profile.show(companion.id)">
    <UserAvatar :user="companion" />
    <div>
      <h5 class="text-primary-light">{{ username }}</h5>
      <p class="text-base-content/80">
        {{ status }}
      </p>
    </div>
  </div>
</template>

<script>
import UserAvatar from "@/components/User/UserAvatar.vue";

export default {
  props: {
    chat: {
      type: Object,
      required: true,
    },
  },

  computed: {
    companion() {
      return this.chat.companion;
    },

    username() {
      return this.companion.full_name || this.companion.username;
    },

    status() {
      return this.companion.status ? "online" : "offline";
    },
  },

  components: { UserAvatar },
};
</script>

<style scoped>
.user-short {
  @apply flex gap-2 items-center truncate cursor-pointer;
}
</style>
