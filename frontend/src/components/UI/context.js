export default {
  props: {
    menu: {
      type: Array,
      required: true,
    },
    show: {
      type: Boolean,
      required: true,
    },
    extraArgs: {
      type: Array,
      default: () => [],
    },
  },

  mounted() {
    this.closeNextClick();
  },

  methods: {
    selected(item) {
      this.$emit("update:show", false);
      item.cb && item.cb(...this.extraArgs);
      this.$nextTick(() => this.$emit("chosen"));
    },
    closeNextClick() {
      if (this.show) {
        document.addEventListener(
          "mouseup",
          () => {
            this.$emit("update:show", false);
          },
          { once: true }
        );
      }
    },
  },

  watch: {
    show(val) {
      this.closeNextClick();
    },
  },
};
