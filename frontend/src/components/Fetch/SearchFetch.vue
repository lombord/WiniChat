<template>
  <slot name="top" />
  <Search class="search-input" v-model="query" />
  <slot name="inBetween" />
  <div ref="fetchElm" class="search-data-box">
    <FetchObserver
      v-if="dataList.length || dataList.size"
      :hasBottom="!!next"
      :fetchBottom="fetchNext"
    >
      <slot name="fetched" :dataList="dataList" />
    </FetchObserver>
    <div v-else class="min-h-[inherit] center-content">
      <slot name="noResult">
        <h2 class="text-secondary text-center">No Result</h2>
      </slot>
    </div>
  </div>
  <slot name="bottom" />
</template>

<script>
import fetchData from "@/mixins/fetchData.js";
import Search from "@/components/Forms/Widgets/Search.vue";

export default {
  expose: ["query", "dataList"],

  data: () => ({
    query: "",
  }),

  props: {
    url: {
      type: String,
      required: true,
    },
    qKey: {
      type: String,
      default: "q",
    },
    initF: {
      type: Function,
      default: null,
    },
    prevF: {
      type: Function,
      default: null,
    },
    nextF: {
      type: Function,
      default: null,
    },
  },

  computed: {
    fetchUrl() {
      return `${this.url}?${this.qKey}=${this.query}`;
    },
  },

  methods: {
    firstAdd(data) {
      const parentAdd = this.initF;
      if (parentAdd) {
        this.dataList = parentAdd(data);
      } else {
        this.dataList = data || [];
      }
    },

    addPrevious(data) {
      const parentPrev = this.prevF;
      if (parentPrev) return parentPrev(data);
      this.dataList.unshift(...data);
    },

    addNext(data) {
      const parentNxt = this.nextF;
      if (parentNxt) return parentNxt(data);
      this.dataList.push(...data);
    },
  },

  watch: {
    query() {
      this.fetchData();
    },
  },

  components: { Search },
  mixins: [fetchData],
  inheritAttrs: false,
};
</script>

<style scoped>
.observer {
  @apply py-4 mt-2 after:loading-spinner;
}

.search-data-box {
  @apply overflow-y-auto overflow-x-hidden min-h-[130px];
}
</style>
