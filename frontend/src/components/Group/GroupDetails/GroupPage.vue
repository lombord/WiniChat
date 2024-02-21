<template>
  <DynamicComps
    excludeCP="EditGroup,"
    :comps="childTabs"
    v-model:current="currTab"
  >
    <template #fallback>
      <GroupTab v-bind="$attrs" boxCls="detail-tab" class="pop-btn-parent flex">
        <template #header>
          <span><i class="fa-solid fa-circle-info"></i></span>
          <span class="max-[475px]:hidden">Info</span>
        </template>
        <template #content>
          <GroupInfo :group="group" class="flex-1" />
          <div class="pop-btn-box">
            <button
              v-if="canEdit"
              @click="currTab = 'editGroup'"
              class="pop-btn"
            >
              <i class="fa-solid fa-pen"></i>
            </button>
          </div>
        </template>
      </GroupTab>
    </template>
  </DynamicComps>
</template>

<script>
import DynamicComps from "@/components/Utils/DynamicComps.vue";
import GroupTab from "../GroupSettings/GroupTab.vue";
import GroupInfo from "./GroupInfo.vue";
import permission from "../GroupRoles/permission.js";

export default {
  data: () => ({
    currTab: null,
  }),

  props: {
    group: {
      type: Object,
      required: true,
    },
  },

  computed: {
    role() {
      return this.group.user_role;
    },

    childTabs() {
      return {
        editGroup: {
          path: "Group/GroupDetails/EditGroup.vue",
          attrs: {
            group: this.group,
          },
        },
      };
    },
  },

  components: { GroupTab, GroupInfo, DynamicComps },
  inheritAttrs: false,
  mixins: [permission],
};
</script>

<style scoped>
.detail-tab {
  @apply gap-0;
}

.detail-tab :deep(.tab-header) {
  @apply bg-opacity-90 z-20 relative;
}
.detail-tab :deep(.tab-content) {
  @apply p-0 overflow-visible;
}
</style>
