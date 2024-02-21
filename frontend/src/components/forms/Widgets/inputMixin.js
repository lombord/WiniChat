export default {
  props: {
    modelValue: {
      required: true,
    },

    maxLength: {
      type: Number,
      default: null,
    },
  },

  computed: {
    value: {
      get() {
        return this.modelValue;
      },
      set(val) {
        const { maxLength } = this;
        if (maxLength != null && val.length > maxLength) {
          val = val.slice(0, maxLength);
        }
        val = this.cleanValue(val);

        this.$refs.input.value = val;
        this.$emit("update:modelValue", val);
      },
    },
  },

  methods: {
    cleanValue(value) {
      return value;
    },
  },
};
