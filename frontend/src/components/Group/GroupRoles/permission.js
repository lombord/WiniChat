// User permission mixin (requires role property)
export default {
  computed: {
    canSend() {
      return this.hasPerm("send_msg");
    },

    permRole() {
      return this.role;
    },

    canDelete() {
      return this.hasPerm("delete_msg");
    },

    canAdd() {
      return this.hasPerm("add_user");
    },

    canEdit() {
      return this.hasPerm("edit_group");
    },

    canManageRole() {
      return this.hasPerm("manage_role");
    },

    isSuperAdmin() {
      return this.permRole?.super_admin;
    },

    isDefaultRole() {
      return this.permRole?.is_default;
    },

    isOwner() {
      return this.permRole?.is_owner;
    },
  },

  methods: {
    hasPriorityOver(role) {
      try {
        const { permRole } = this;
        return (
          !role.is_owner &&
          (permRole.is_owner || permRole.priority < role.priority)
        );
      } catch (error) {
        return false;
      }
    },

    hasPerm(perm) {
      try {
        const role = this.permRole;
        return role[perm] || role.super_admin || role.is_owner;
      } catch (error) {
        return false;
      }
    },

    hasPermOver(role, perm) {
      return this.hasPerm(perm) && this.hasPriorityOver(role);
    },

    canKick(role) {
      return this.hasPermOver(role, "kick_user");
    },

    canBan(role) {
      return this.hasPermOver(role, "ban_user");
    },
  },
};
