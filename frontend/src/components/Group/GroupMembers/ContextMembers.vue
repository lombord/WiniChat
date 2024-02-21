<template>
  <div class="flex flex-col gap-1.5" :class="$attrs.class">
    <TransitionGroup name="item-down">
      <Member
        v-memo="[members.length]"
        v-for="member in members"
        class="ctx-member"
        @contextmenu.prevent.stop="(e) => toggleCtx(member, e)"
        v-bind="$utils.exclude($attrs, ['class'])"
        :group="group"
        :key="member.id"
        :member="member"
      />
    </TransitionGroup>
    <ContextManager
      v-model:show="showCtx"
      ref="context"
      :menu="ctxMenu"
      class="context-menu"
    />
  </div>
</template>

<script>
import { computed } from "vue";

import ContextManager from "@/components/Utils/ContextManager.vue";
import Member from "./Member.vue";
import permission from "../GroupRoles/permission.js";

export default {
  data: () => ({
    showCtx: false,
    currMember: null,
    ctxMenu: null,
  }),

  props: {
    members: {
      required: true,
    },

    group: {
      type: Object,
      required: true,
    },
  },

  computed: {
    showContext() {
      return this.$refs.context.showContext;
    },

    role() {
      return this.group.user_role;
    },

    socket() {
      return this.$session.socket;
    },

    currRole() {
      if (this.currMember) {
        return this.currMember.role;
      }
    },
  },

  created() {
    this.ctxMenu = [
      {
        label: "Profile",
        icon: "fa-solid fa-user",
        cb: () => this.$profile.show(this.currMember.user.id),
      },
      {
        label: "Role",
        icon: "fa-solid fa-user-shield",
        hidden: computed(() => !this.hasPermOver(this.currRole, "manage_role")),
        path: "Group/GroupRoles/SearchRole",
        nested: {
          group: computed(() => this.group),
          currRoleId: computed(() => this.currRole?.id),
          chooseCB: this.changeRole,
        },
      },

      {
        label: "Kick",
        icon: "fa-solid fa-user-xmark",
        cls: "text-error",
        hidden: computed(() => !this.canKick(this.currRole)),
        cb: this.kickMember,
      },

      {
        label: "Ban",
        icon: "fa-solid fa-user-lock",
        cls: "text-error",
        hidden: computed(() => !this.canBan(this.currRole)),
        cb: this.banMember,
      },
    ];
  },

  methods: {
    async toggleCtx(member, evt) {
      const elm = await this.showContext(evt);
      const session = this.$session;
      this.currMember = member;
      if (!member.role.fetched) {
        const prom = session.getWSRole(this.group, member.role.id);
        await session.animate(prom, elm);
      }
    },

    leaveCommon(user_id, event = "leave", data = null) {
      data = data || { user_id };
      const {
        socket,
        group: { id: group_id },
      } = this;
      socket.groupMessage("remove_members", { group_id, data: [user_id] });
      socket.sendGroupEvent({
        event,
        group_id,
        ...data,
      });
      this.currMember = null;
    },

    async kickMember() {
      const member = this.currMember;
      if (!member) return;
      try {
        await this.$session.delete(member.url);
      } catch (error) {
        this.$flashes.axiosError(error);
        return;
      }
      this.leaveCommon(member.user.id);
    },

    async banMember() {
      const member = this.currMember;
      if (!member) return;
      const userId = member.user.id;
      let data = null;
      try {
        ({ data } = await this.$session.post(`${this.group.url}bans/`, {
          user: userId,
        }));
      } catch (error) {
        this.$flashes.axiosError(error);
        return;
      }
      this.leaveCommon(userId, "ban", { ban: data });
    },

    async changeRole({ id: role }) {
      const session = this.$session;
      const member = this.currMember;
      try {
        const { data } = await session.patch(member.url, { role });
        const sendData = {
          event: "role_change",
          group_id: this.group.id,
          user_id: member.user.id,
          data: data.role,
        };
        session.socket.sendGroupEvent(sendData);
        session.socket.changeMemberRole(sendData);
        this.currMember = null;
      } catch (error) {
        this.$flashes.axiosError(error);
      }
    },
  },

  components: { Member, ContextManager },
  mixins: [permission],
};
</script>

<style scoped>
.ctx-member.active-context {
  @apply bg-primary-medium/90;
}

.ctx-member.active-context :deep(*) {
  @apply text-white/90 !important;
}
</style>
