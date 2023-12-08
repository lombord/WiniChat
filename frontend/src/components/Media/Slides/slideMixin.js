export default {
  props: {
    files: {
      type: Array,
      required: true,
    },
    index: {
      type: Number,
      default: 0,
    },
  },

  computed: {
    current() {
      return this.files[this.currIdx];
    },
    length() {
      return this.files.length;
    },
    maxIdx() {
      return this.length - 1;
    },
    isLast() {
      return this.currIdx == this.maxIdx;
    },
    currIdx: {
      get() {
        return this.index;
      },
      set(val) {
        this.$emit("update:index", this.validateIdx(val));
      },
    },
  },

  methods: {
    validateIdx(val) {
      const { min, max } = Math;
      return max(0, min(val, this.maxIdx));
    },
  },
};
