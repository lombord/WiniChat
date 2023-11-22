<template>
  <input :min="min" :max="max" type="range" class="my-range" v-model="value" />
</template>

<script>
export default {
  props: {
    modelValue: {
      required: true,
    },
    min: {
      type: Number,
      default: 0,
    },
    max: {
      type: Number,
      default: 1,
    },
  },

  computed: {
    value: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:modelValue", Number(value));
      },
    },
  },

  mounted() {
    this.updatePercent();
  },

  methods: {
    updatePercent() {
      const percent = (this.value * 100) / (this.max || 1);
      this.$el.style.setProperty("--percent", percent);
    },
  },

  watch: {
    value() {
      this.updatePercent();
    },
  },
};
</script>

<style scoped>
.my-range {
  --color1: theme("backgroundColor.primary");
  --color2: theme("backgroundColor.base-200");
  @apply appearance-none transition-[opacity]
  opacity-75 rounded-full h-1.5 cursor-pointer
  hover:opacity-100;
  --percent: 0;
  background: linear-gradient(
    to right,
    var(--color1) calc(var(--percent) * 1% + 2px),
    var(--color2) calc(var(--percent) * 1%)
  );
}

.range-thumb {
  @apply bg-[--color1] rounded-full 
  opacity-0 transition 
  active:scale-125;
}

.my-range::-webkit-slider-thumb {
  @apply appearance-none w-2 p-2 range-thumb;
}
.my-range:hover::-webkit-slider-thumb {
  @apply opacity-100;
}

.my-range::-moz-range-thumb {
  @apply range-thumb border-none;
}
.my-range:hover::-moz-range-thumb {
  @apply opacity-100;
}
</style>
