<template>
  <div ref="fetchElm" class="data-content">
    <template v-if="dataList.length">
      <DynamicComp
        @loaded="compLoaded = true"
        :[passAs]="dataList"
        v-bind="$attrs"
      />
      <div v-if="compLoaded" v-int="fetchNext">
        <div class="load-anim observer"></div>
      </div>
    </template>
    <slot v-else name="noResult">
      <h5 class="text-secondary">No Result</h5>
    </slot>
  </div>
</template>

<script>
import fetchData from "@/mixins/fetchData.js";
import DynamicComp from "@/components/Utils/DynamicComp.vue";

export default {
  data: () => ({
    compLoaded: false,
  }),

  props: {
    url: {
      type: String,
      required: true,
    },
    passAs: {
      type: String,
      required: true,
    },
  },

  computed: {
    fetchUrl() {
      return this.url;
    },
  },
  inheritAttrs: false,
  components: { DynamicComp },
  mixins: [fetchData],
};
</script>

<style scoped>
.data-content {
  @apply overflow-x-hidden;
}

.data-content.load-anim::after {
  @apply loading-ring;
}

.observer.load-anim {
  @apply pt-10 mt-6 after:loading-spinner;
}
</style>
