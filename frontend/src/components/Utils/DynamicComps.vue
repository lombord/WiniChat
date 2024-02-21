<template>
  <KeepAlive :max="maxCache" :include="includeCP" :exclude="excludeCP">
    <slot v-if="loading" :name="fallbackName">
      <div class="load-anim fallback-load"></div>
    </slot>
    <component
      v-else
      :is="currComp"
      @close="clearCurrent"
      :key="attrs?.key || current"
      v-bind="{ ...$attrs, ...attrs }"
    />
  </KeepAlive>
  <KeepAlive>
    <TagComp v-if="!currObj">
      <slot name="fallback" />
    </TagComp>
  </KeepAlive>
</template>

<script>
import DynamicComp from "./DynamicComp.vue";
import TagComp from "./TagComp.vue";

export default {
  data: () => ({
    currComp: null,
    loading: false,
  }),

  props: {
    comps: {
      type: Object,
      required: true,
    },
    current: {
      type: [String, null],
      required: true,
    },
    maxCache: {
      type: Number,
      default: 5,
    },
    includeCP: {
      type: [String, Array, RegExp],
      default: null,
    },
    excludeCP: {
      type: [String, Array, RegExp],
      default: null,
    },
  },

  computed: {
    currObj() {
      return this.comps[this.current];
    },
    path() {
      return this.currObj?.path;
    },
    attrs() {
      return this.currObj?.attrs;
    },
    fallbackName() {
      return `${this.current}FB`;
    },
  },

  created() {
    this.loadComp();
  },

  methods: {
    clearCurrent() {
      this.$emit("update:current", null);
    },

    async loadComp() {
      const { path } = this;
      if (path) {
        this.loading = true;
        this.currComp = await this.$utils.compImport(path);
        this.loading = false;
      } else {
        this.currComp = null;
      }
    },
  },

  watch: {
    path(val, old) {
      val != old && this.loadComp();
    },
  },

  emits: ["update:current"],
  inheritAttrs: false,
  components: { TagComp, DynamicComp },
};
</script>

<style scoped>
.comp-enter-active,
.comp-leave-active {
  @apply transition;
}

.comp-enter-from,
.comp-leave-to {
  @apply opacity-0 scale-[1.02];
}
</style>
