<template>
  <div
    :class="$attrs.class"
    v-if="!showImg"
    class="img-placeholder load-anim"
  ></div>
  <img
    ref="image"
    loading="lazy"
    :class="{ 'img-loading': !showImg }"
    :src="src"
    v-bind="$attrs"
    @load="onLoad"
  />
</template>

<script>
export default {
  data: () => ({
    loaded: false,
  }),

  props: {
    src: {
      type: String,
      default: null,
    },
  },

  computed: {
    showImg() {
      return this.src && this.loaded;
    },
  },

  mounted() {
    this.$emit("imgLoad", this.$refs.image);
  },

  methods: {
    onLoad() {
      this.loaded = true;
    },
  },

  emits: ["imgLoad"],

  watch: {
    src(val, old) {
      if (old !== val) {
        this.loaded = false;
      }
    },
  },

  inheritAttrs: false,
};
</script>

<style scoped>
.img-placeholder {
  @apply after:loading-ring w-full h-full;
}

.img-loading {
  @apply w-0 h-0 invisible !important;
}
</style>
