<template>
  <div class="tabs-root">
    <Tabs :tabs="tabs" v-model="current" />
    <div class="fetch-box">
      <KeepAlive>
        <component
          v-if="!currTab.manual"
          :key="current"
          is="FetchData"
          v-bind="currTab"
        >
          <template #noResult>
            <h3 class="text-5xl text-secondary text-center">
              <i class="bi bi-folder-x"></i>
            </h3>
          </template>
        </component>
        <template v-else>
          <DynamicComp :key="current" v-bind="currTab.attrs" />
        </template>
      </KeepAlive>
    </div>
  </div>
</template>

<script>
import Tabs from "@/components/UI/Tabs.vue";
import FetchData from "./FetchData.vue";
import DynamicComp from "@/components/Utils/DynamicComp.vue";

export default {
  data: () => ({
    current: null,
  }),

  props: {
    tabsMap: {
      type: Object,
      required: true,
    },
  },
  computed: {
    tabs() {
      return Object.keys(this.tabsMap);
    },
    currTab() {
      return this.tabsMap[this.current];
    },
  },

  created() {
    this.current = this.tabs[0];
  },

  components: { Tabs, FetchData, DynamicComp },
};
</script>

<style scoped>
.tabs-root {
  @apply flex flex-col gap-3 overflow-hidden 
  min-h-screen max-h-screen pb-2;
}

.fetch-box {
  @apply overflow-x-hidden rounded-xl;
}

.fetch-box :deep(.load-anim) {
  @apply min-h-20;
}

.fetch-box :deep(.load-anim::after) {
  @apply loading-ring;
}

@supports not selector(::-webkit-scrollbar) {
  .fetch-box {
    scrollbar-width: none;
  }
}

.fetch-box::-webkit-scrollbar {
  @apply hidden;
}

:deep(.dynamic-flex) {
  --min-size: 180px;
  @apply gap-0.5;
}

:deep(.dynamic-flex > *) {
  @apply h-[250px];
}
</style>
