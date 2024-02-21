<template>
  <DynamicComps
    v-model:current="currTab"
    excludeCP="CreateRole,RoleTab"
    :comps="childTabs"
    @roleCreated="addNewRole"
    @removeRole="removeRole"
  >
    <template #fallback>
      <GroupTab
        v-bind="$attrs"
        class="p-3 pt-0"
        boxCls="tabRoot pop-btn-parent"
      >
        <template #header>
          <span><i class="fa-solid fa-shield-halved"></i></span>
          <span class="max-[475px]:hidden">Roles</span>
        </template>
        <template #content>
          <SearchFetch
            ref="fetchCtrl"
            :initF="initRoles"
            :nextF="addRoles"
            :url="url"
          >
            <template #fetched>
              <RolesList
                class="flex-1"
                @chosen="changeRole"
                :roles="sortedRoles"
                :group="group"
              />
            </template>
          </SearchFetch>
        </template>
        <template #bottom>
          <div class="pop-btn-box">
            <button
              v-if="canManageRole"
              @click="currTab = 'createRole'"
              class="pop-btn"
            >
              <i class="fa-solid fa-plus"></i>
            </button>
          </div>
        </template>
      </GroupTab>
    </template>
  </DynamicComps>
</template>

<script>
import SearchFetch from "@/components/Fetch/SearchFetch.vue";
import DynamicComps from "@/components/Utils/DynamicComps.vue";
import GroupTab from "../GroupSettings/GroupTab.vue";

import RolesList from "./RolesList.vue";
import permission from "./permission.js";

export default {
  data: () => ({
    currTab: null,
    rolesMap: null,
    currRole: null,
  }),

  props: {
    group: {
      type: Object,
      required: true,
    },
  },

  computed: {
    url() {
      return `${this.group.url}roles/`;
    },

    query() {
      return this.$refs.fetchCtrl.query;
    },

    childTabs() {
      const currRole = this.currRole;
      return {
        createRole: {
          path: "Group/GroupRoles/CreateRole.vue",
          attrs: {
            group: this.group,
          },
        },
        roleTab: {
          path: "Group/GroupRoles/RoleTab.vue",
          attrs: {
            group: this.group,
            role: currRole,
            key: `role:${currRole?.id}`,
          },
        },
      };
    },

    sortedRoles() {
      const roles = Array.from(this.rolesMap.values());
      if (this.query) {
        return roles;
      }
      roles.sort(({ priority: p1 }, { priority: p2 }) => p1 - p2);
      return roles;
    },

    role() {
      return this.group.user_role;
    },

    socket() {
      return this.$session.socket;
    },
  },

  created() {
    const {
      socket,
      group: { id },
    } = this;
    socket.onGroup(id, "new_role", this.addNewRole);
    socket.onGroup(id, "del_role", this.rmWSRole);
  },

  beforeUnmount() {
    const {
      socket,
      group: { id },
    } = this;
    socket.rmGroupEvent(id, "new_role", this.addNewRole);
    socket.rmGroupEvent(id, "del_role", this.rmWSRole);
  },

  methods: {
    initRoles(data) {
      this.rolesMap = new Map();
      this.addRoles(data);
      return this.rolesMap;
    },

    addNewRole(role) {
      if (role && this.rolesMap && !this.query) {
        this.rolesMap.set(role.id, role);
      }
    },

    addRoles(roles) {
      const roleM = this.rolesMap;
      for (const role of roles) {
        roleM.set(role.id, role);
      }
    },

    rmWSRole(data, { role_id }) {
      this.removeRole(role_id);
    },

    removeRole(roleId) {
      this.rolesMap.delete(roleId);
    },

    changeRole(role) {
      this.currRole = role;
      this.currTab = "roleTab";
    },
  },

  inheritAttrs: false,

  components: { GroupTab, SearchFetch, RolesList, DynamicComps, DynamicComps },
  mixins: [permission],
};
</script>

<style scoped>
.tabRoot {
  @apply relative;
}
</style>
