<template>
  <div class="col-flex roles-box">
    <TransitionGroup name="role">
      <Role
        v-for="role in roles"
        :key="role.id"
        :role="role"
        :group="group"
        @click="$emit('chosen', role)"
      />
    </TransitionGroup>
  </div>
</template>

<script>
import Role from "./Role.vue";

export default {
  props: {
    roles: {
      type: Array,
      required: true,
    },
    group: {
      type: Object,
      required: true,
    },
  },

  components: { Role, Role },
  emits: ["chosen"],
};
</script>

<style scoped>
.roles-box {
  @apply gap-1.5;
}

.roles-box > * {
  @apply transition active:scale-[0.97];
}

.roles-box:deep(> *:last-child .role-perms > *) {
  @apply tooltip-top;
}

.role-enter-active,
.role-leave-active {
  @apply transition;
}

.role-enter-from,
.role-leave-to {
  @apply translate-y-6 opacity-0;
}
</style>
