<template>
  <div class="role-box click-scale">
    <div class="role-type center-content">
      <i v-if="isOwner" class="fa-solid fa-user-astronaut text-secondary"></i>
      <i v-else-if="isDefaultRole" class="fa-solid fa-user"></i>
      <i v-else-if="isSuperAdmin" class="fa-solid fa-user-tie"></i>
      <i v-else class="fa-solid fa-user-shield"></i>
    </div>
    <div class="col-flex gap-1 flex-1">
      <h6 class="text-base-content/95">{{ role.name }}</h6>
      <div class="role-perms">
        <TransitionGroup name="pop">
          <template v-for="{ perm, hint, icon } in permBubbles" :key="perm">
            <div v-if="hasPerm(perm)" class="tooltip" :data-tip="hint">
              <span>
                <i :class="icon"></i>
              </span>
            </div>
          </template>
        </TransitionGroup>
      </div>
    </div>
    <div class="priority-wrap center-content">
      <p class="font-bold">
        {{ role.priority }}
      </p>
    </div>
  </div>
</template>

<script>
import trackRole from "./trackRole.js";
import permission from "./permission.js";

export default {
  data: () => ({
    permBubbles: [
      {
        perm: "send_msg",
        hint: "send message",
        icon: "bi bi-chat-left-dots-fill",
      },
      {
        perm: "delete_msg",
        hint: "del message",
        icon: "fa-solid fa-trash-can text-error",
      },
      {
        perm: "add_user",
        hint: "add user",
        icon: "fa-solid fa-user-plus",
      },
      {
        perm: "kick_user",
        hint: "kick user",
        icon: "fa-solid fa-user-large-slash text-error",
      },
      {
        perm: "ban_user",
        hint: "ban user",
        icon: "fa-solid fa-user-lock text-base-content",
      },
      {
        perm: "unban_user",
        hint: "unban user",
        icon: "fa-solid fa-user-check text-success",
      },
      {
        perm: "edit_group",
        hint: "edit group",
        icon: "fa-solid fa-pen-to-square text-secondary",
      },
      {
        perm: "manage_role",
        hint: "manage role",
        icon: "fa-solid fa-user-shield text-accent",
      },
    ],
  }),

  props: {
    role: {
      type: Object,
      required: true,
    },
    group: {
      type: Object,
      required: true,
    },
  },

  computed: {
    groupId() {
      return this.group.id;
    },
  },

  mixins: [trackRole, permission],
};
</script>

<style scoped>
.role-box {
  @apply py-1.5 p-2 bg-base-300/50 flex gap-2 cursor-pointer
  items-center rounded-2xl hover:bg-base-content/15;
}

.role-type {
  @apply text-2xl text-accent w-14 bg-base-content/10
  aspect-square rounded-full;
}

.role-perms {
  @apply flex gap-1 items-center flex-wrap;
}

.role-perms > * {
  @apply text-info w-7 text-sm flex flex-col  
  items-center aspect-square transition
  hover:scale-110 tooltip tooltip-open 
  tooltip-bottom justify-center
  rounded-full bg-base-content/[6%];
  --tooltip-color: theme(colors.base-content);
  --tooltip-text-color: theme(colors.base-100);
}

.priority-wrap {
  @apply text-info p-0.5 px-2 rounded-full 
  bg-base-content/[6%] min-w-7;
}
</style>
