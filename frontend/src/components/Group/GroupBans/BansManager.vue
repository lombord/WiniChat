<template>
  <div class="col-flex gap-1.5">
    <TransitionGroup name="item-down">
      <BannedUser
        v-for="ban in bans"
        class="banned-user"
        @contextmenu.prevent.stop="(e) => toggleCtx(ban, e)"
        :key="ban.user.id"
        :ban="ban"
      />
    </TransitionGroup>
    <ContextManager
      v-model:show="showCtx"
      ref="context"
      :menu="banCtx"
      class="context-menu"
    />
  </div>
</template>

<script>
import ContextManager from "@/components/Utils/ContextManager.vue";
import BannedUser from "./BannedUser.vue";

export default {
  data: () => ({
    showCtx: false,
    banCtx: null,
    currBan: null,
  }),

  props: {
    bans: {
      required: true,
    },
    group: {
      type: Object,
      required: true,
    },
  },

  computed: {
    currUser() {
      return this.currBan?.user;
    },

    showContext() {
      return this.$refs.context.showContext;
    },
  },

  created() {
    this.banCtx = [
      {
        label: "Profile",
        icon: "fa-solid fa-user",
        cb: () => this.$profile.show(this.currUser.id),
      },
      {
        label: "Unban",
        cls: "text-success",
        icon: "fa-solid fa-user-check",
        cb: this.unbanUser,
      },
    ];
  },

  methods: {
    async toggleCtx(ban, evt) {
      this.currBan = ban;
      await this.showContext(evt);
    },

    async unbanUser() {
      const session = this.$session;
      const socket = session.socket;
      const ban = this.currBan;
      try {
        await session.delete(ban.url);
        const [group_id, user_id] = [this.group.id, ban.user.id];
        socket.groupMessage("unban", { group_id, data: user_id });
        socket.sendGroupEvent({ event: "unban", group_id, user_id });
      } catch (error) {
        this.$flashes.axiosError(error);
      }
    },
  },

  components: { BannedUser, ContextManager },
};
</script>

<style scoped></style>
