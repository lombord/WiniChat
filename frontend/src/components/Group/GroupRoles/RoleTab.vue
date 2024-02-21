<template>
  <GroupTab class="role-tab-content" boxCls="gap-0" @close="$emit('close')">
    <template #header>
      <span>
        <i class="fa-solid fa-user-shield"></i>
      </span>
      <span>{{ role.name }}</span>
    </template>
    <template #content>
      <RoleForm
        ref="roleForm"
        :group="group"
        :config="editCfg"
        :isEditForm="true"
        :getPromElm="() => $refs.saveBtn"
        :disabled="!editing"
        successMessage="Role has been edited"
        class="form-box"
        :editRole="role"
        @succeed="roleUpdated"
      >
        <template #submitBtn>
          <div class="buttons-box dynamic-grid" v-if="canManageOver">
            <template v-if="!editing">
              <button
                v-if="!isSpecialRole"
                @click="delRole"
                type="button"
                class="role-btn del-btn spinner-on-load"
              >
                <span><i class="fa-solid fa-trash"></i></span>
                <span>Delete</span>
              </button>
              <button @click="editing = true" type="button" class="role-btn">
                <span><i class="fa-solid fa-pen"></i></span>
                <span>Edit</span>
              </button>
            </template>
            <template v-else>
              <button
                @click="cancelEdit"
                type="button"
                class="role-btn del-btn"
              >
                <span><i class="fa-solid fa-ban"></i></span>
                <span>Cancel</span>
              </button>
              <button ref="saveBtn" type="submit" class="submit-btn role-btn">
                <span><i class="fa-solid fa-pen"></i></span>
                <span>Save</span>
              </button>
            </template>
          </div>
          <span class="hidden"></span>
        </template>
      </RoleForm>
    </template>
  </GroupTab>
</template>

<script>
import GroupTab from "../GroupSettings/GroupTab.vue";
import RoleForm from "./RoleForm.vue";
import permission from "./permission.js";

export default {
  name: "RoleTab",
  data: () => ({
    editing: false,
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
    isSpecialRole() {
      const { role } = this;
      return role.is_default || role.is_owner;
    },

    editCfg() {
      return {
        method: "patch",
        url: this.role.url,
      };
    },
    canManageOver() {
      return this.hasPermOver(this.role, "manage_role");
    },

    permRole() {
      return this.group.user_role;
    },
  },

  methods: {
    cancelEdit() {
      this.editing = false;
      this.$refs.roleForm.setInitial();
    },

    async delRole({ currentTarget }) {
      try {
        const { role } = this;
        const session = this.$session;
        const prom = session.delete(role.url);
        const { data: new_role } = await session.animate(prom, currentTarget);
        session.socket.sendGroupEvent({
          event: "role_del",
          group_id: this.group.id,
          role_id: role.id,
          new_role,
        });
        this.$emit("removeRole", role.id);
        this.$emit("close");
      } catch (error) {
        console.log(error);
      }
    },

    roleUpdated(response, data) {
      const { socket } = this.$session;
      const group_id = this.group.id;
      const role_id = this.role.id;
      socket.sendGroupEvent({
        event: "role_update",
        group_id,
        role_id,
        data,
      });
      socket.refreshRole(group_id, role_id, data);
      this.$emit("close");
    },
  },

  watch: {
    canManageOver(val) {
      if (!val && this.editing) {
        this.editing = false;
      }
    },
  },

  components: { GroupTab, RoleForm },
  mixins: [permission],
  emits: ["removeRole", "close"],
};
</script>

<style scoped>
@import "@/assets/main.css";
@import "@/assets/animations.css";

:deep(.role-tab-content) {
  @apply overflow-y-auto p-0;
}

.form-box {
  @apply px-2 sm:px-4 md:px-10 pb-8 pt-10 bg-base-300;
}

.buttons-box {
  --min-size: 150px;
  --repeat-mode: auto-fit;
  /* @apply 1; */
}

.role-btn {
  @apply w-btn click-anim;
}

.role-btn {
  @apply btn-primary flex gap-1 items-center;
}

.del-btn {
  @apply btn-error !important;
}
</style>
