<template>
  <Transition name="pop">
    <div class="col-flex search-wrapper">
      <SearchFetch :url="rolesUrl">
        <template #fetched="{ dataList }">
          <div>
            <TransitionGroup name="pop">
              <template v-for="role in dataList" :key="role.id">
                <RoleItem
                  v-if="hasPermOver(role, 'manage_role')"
                  :isCurrent="currRoleId == role.id"
                  @chosen="changeRole"
                  :role="role"
                />
              </template>
            </TransitionGroup>
          </div>
        </template>
        <template #noResult>
          <h5 class="text-secondary text-center">No Result</h5>
        </template>
      </SearchFetch>
    </div>
  </Transition>
</template>

<script>
import SearchFetch from "@/components/Fetch/SearchFetch.vue";
import permission from "../permission.js";
import RoleItem from "./RoleItem.vue";

export default {
  data: () => ({
    currProm: null,
  }),

  props: {
    show: {
      type: Boolean,
      required: true,
    },
    group: {
      type: Object,
      required: true,
    },

    chooseCB: {
      type: Function,
      required: true,
    },

    currRoleId: {
      required: true,
    },
  },

  computed: {
    rolesUrl() {
      return `${this.group.url}role-options/`;
    },

    role() {
      return this.group.user_role;
    },
  },

  methods: {
    async changeRole(role, option) {
      if (this.currProm || this.currRoleId == role.id) return;
      option.loading = true;
      try {
        const prom = (this.currProm = this.chooseCB(role));
        await prom;
      } finally {
        option.loading = false;
        this.currProm = null;
        this.$emit("update:show", false);
      }
    },
  },

  components: { SearchFetch, RoleItem },
  mixins: [permission],
};
</script>

<style scoped>
.search-wrapper {
  @apply gap-1 max-h-[200px];
}
.search-wrapper :deep(.search-input) {
  @apply py-1.5 border;
}

.search-wrapper :deep(.search-data-box) {
  @apply min-h-[70px];
}
.search-wrapper :deep(.search-root) {
  @apply text-sm;
}
</style>
