<template>
  <GroupTab class="overflow-y-auto p-0" boxCls="gap-0">
    <template #header>
      <span>
        <i class="fa-solid fa-shield-halved"></i>
      </span>
      Create Role
    </template>
    <template #content>
      <template v-if="canManageRole">
        <RoleForm
          :group="group"
          :config="roleCfg"
          submitLabel="Create"
          successMessage="Role has been created"
          class="px-10 pb-8 pt-10 bg-base-300"
          @succeed="roleCreated"
        />
      </template>
      <div v-else>
        <h4 class="text-error">You are not allowed here</h4>
      </div>
    </template>
  </GroupTab>
</template>

<script>
import GroupTab from "../GroupSettings/GroupTab.vue";
import RoleForm from "./RoleForm.vue";
import accessRequired from "./accessRequired.js";

export default {
  name: "CreateRole",

  data: () => ({
    accessPerm: "manage_role",
  }),

  props: {
    group: {
      type: Object,
      required: true,
    },
  },

  computed: {
    roleCfg() {
      return {
        method: "post",
        url: `${this.group.url}roles/`,
      };
    },

    role() {
      return this.group.user_role;
    },
  },

  methods: {
    roleCreated({ data }) {
      this.$session.socket.sendGroupEvent({
        group_id: this.group.id,
        event: "new_role",
        role: data,
      });
      this.$emit("roleCreated", data);
      this.$emit("close");
    },
  },

  components: { GroupTab, RoleForm },
  emits: ["roleCreated"],
  mixins: [accessRequired],
};
</script>

<style scoped></style>
