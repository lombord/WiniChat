<template>
  <GroupTab class="overflow-x-hidden">
    <template #header>
      <span>
        <i class="fa-solid fa-user-lock"></i>
      </span>
      <span class="max-[475px]:hidden">Bans</span>
    </template>
    <template #content>
      <SearchFetch ref="search" :url="fetchUrl">
        <template #fetched="{ dataList }">
          <BansManager :bans="dataList" :group="group" />
        </template>
      </SearchFetch>
    </template>
  </GroupTab>
</template>

<script>
import SearchFetch from "@/components/Fetch/SearchFetch.vue";
import accessRequired from "../GroupRoles/accessRequired.js";
import GroupTab from "../GroupSettings/GroupTab.vue";
import BansManager from "./BansManager.vue";

export default {
  data: () => ({
    accessPerm: "unban_user",
  }),

  props: {
    group: {
      type: Object,
      required: true,
    },
  },

  computed: {
    fetchUrl() {
      return `${this.group.url}bans`;
    },

    bans() {
      return this.$refs.search.dataList;
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

    socket.onGroup(id, "ban", this.addBan);
    socket.onGroup(id, "unban", this.removeBan);
  },

  beforeUnmount() {
    const {
      socket,
      group: { id },
    } = this;
    socket.rmGroupEvent(id, "ban", this.addBan);
    socket.rmGroupEvent(id, "unban", this.removeBan);
  },

  methods: {
    addBan(ban) {
      this.bans.unshift(ban);
    },

    removeBan(userId) {
      const { bans } = this;
      if (!bans) return;
      const idx = bans.findIndex(({ user }) => user.id == userId);
      if (idx >= 0) {
        bans.splice(idx, 1);
      }
    },
  },

  components: { GroupTab, SearchFetch, BansManager },
  mixins: [accessRequired],
};
</script>

<style scoped></style>
