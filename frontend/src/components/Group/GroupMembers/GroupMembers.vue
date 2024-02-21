<template>
  <GroupTab class="members-root">
    <template #header>
      <span><i class="fa-solid fa-user-group"></i></span>
      <span class="hidden sm:block">Members</span>
    </template>
    <template #content>
      <SearchFetch
        ref="search"
        :url="fetchUrl"
        :initF="initMembers"
        :nextF="addMembers"
      >
        <template #fetched>
          <ContextMembers
            class="flex-1"
            :members="cleanedMembers"
            :group="group"
          />
        </template>
      </SearchFetch>
    </template>
  </GroupTab>
</template>

<script>
import SearchFetch from "@/components/Fetch/SearchFetch.vue";
import GroupTab from "../GroupSettings/GroupTab.vue";

import ContextMembers from "./ContextMembers.vue";
import trackMembers from "./trackMembers.js";

export default {
  computed: {
    query() {
      return this.$refs.search.query;
    },

    cleanedMembers() {
      if (this.hasQuery) {
        return this.members.values();
      } else {
        return this.sortedMembers;
      }
    },

    hasQuery() {
      const { query } = this;
      return !!(query && query.trim());
    },
  },

  methods: {
    addWSMembers(data) {
      if (!this.hasQuery) {
        this.addMembers(data);
      }
    },
  },

  components: { ContextMembers, SearchFetch, GroupTab },
  mixins: [trackMembers],
};
</script>

<style scoped>
:deep(.members-root) {
  @apply relative gap-1.5;
}

:deep(.member-box) {
  @apply bg-base-300/60;
}

.btn-box {
  @apply flex justify-end pointer-events-none 
  p-4 absolute bottom-0 inset-x-0 z-10;
}

.btn-box > * {
  @apply pointer-events-auto;
}

.btn-back {
  @apply text-4xl rounded-full
  transition px-[18px] opacity-0 backdrop-blur-xl
  scale-50;
}

.members-root:hover .btn-back {
  @apply opacity-100 scale-100;
}

.members-root:hover .btn-back:active {
  @apply scale-95;
}
</style>
