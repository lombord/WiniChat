<template>
  <div class="widget-box" :disabled="disabled">
    <button type="button" @click="value -= step" class="num-btn">
      <i class="fa-solid fa-minus"></i>
    </button>
    <input
      ref="input"
      type="number"
      class="number-input"
      v-bind="$attrs"
      v-model="value"
      :min="min"
      :max="max"
      :step="step"
    />
    <button type="button" @click="value += step" class="num-btn">
      <i class="fa-solid fa-plus"></i>
    </button>
  </div>
</template>

<script>
import inputMixin from "./inputMixin.js";
export default {
  props: {
    min: {
      type: Number,
      default: null,
    },
    max: {
      typeof: Number,
      default: null,
    },
    step: {
      typeof: Number,
      default: 1,
    },

    disabled: {
      type: Boolean,
      default: false,
    },
  },

  methods: {
    cleanValue(val) {
      if (val == null || isNaN(val)) {
        val = this.min;
      }
      val = this.$utils.range(val, this.min, this.max);
      val -= val % this.step;
      return val;
    },
  },

  watch: {
    max() {
      this.value = this.value;
    },
    min() {
      this.value = this.value;
    },
    sep() {
      this.value = this.value;
    },
  },

  inheritAttrs: false,

  mixins: [inputMixin],
};
</script>

<style scoped>
.widget-box {
  @apply grid grid-cols-4 rounded-xl overflow-hidden;
}

.num-btn {
  @apply transition text-xl btn-primary block;
}

.widget-box[disabled="true"] .num-btn {
  @apply btn-disabled bg-base-content/50 opacity-80;
}

.num-btn:active {
  @apply bg-primary-medium;
}

.number-input {
  @apply outline-none col-span-2 
  border-y border-base-content/20
  text-center text-2xl w-full bg-base-100;
}

.widget-box[disabled="true"] .number-input {
  @apply bg-base-200 text-base-content/60;
}

.number-input::-webkit-outer-spin-button,
.number-input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.number-input {
  -moz-appearance: textfield;
}
</style>
