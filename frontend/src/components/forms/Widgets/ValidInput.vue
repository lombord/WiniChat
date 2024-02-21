<template>
  <div class="valid-box" :class="{ 'valid-disabled': disabled }">
    <PHInput
      v-bind="$attrs"
      :modelValue="modelValue"
      :disabled="disabled"
      wrapCls="w-full"
    />
    <div ref="result" class="result-box center-content">
      <Transition name="pop" mode="out-in">
        <i v-if="isValid" class="fa-solid fa-circle-check text-success"></i>
        <i v-else class="fa-solid fa-circle-xmark text-error"></i>
      </Transition>
    </div>
  </div>
</template>

<script>
import PHInput from "./PHInput.vue";
import abortController from "@/mixins/abortController.js";
import safeRequest from "@/mixins/safeRequest.js";
import axios from "axios";

export default {
  data() {
    return {
      isValid: true,
      tId: null,
      initialVal: this.modelValue,
    };
  },

  props: {
    checkUrl: {
      type: String,
      required: true,
    },
    modelValue: {
      required: true,
    },
    queryKey: {
      type: String,
      default: "q",
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },

  computed: {
    queryUrl() {
      return `${this.checkUrl}?${this.queryKey}=${this.modelValue}`;
    },
  },

  methods: {
    async validateValue() {
      if (this.disabled) return;
      const { modelValue } = this;
      if (!modelValue) {
        this.isValid = false;
        return;
      } else if (modelValue == this.initialVal) {
        this.isValid = true;
        return;
      }
      const { signal } = this.getNewController();
      try {
        const prom = this.request({ url: this.queryUrl, signal });
        const elm = this.$refs.result;
        const { data } = await this.$session.animate(prom, elm);
        this.isValid = data.is_valid;
      } catch (error) {
        if (!axios.isCancel(error)) {
          this.$flashes.axiosError(error);
        }
      }
    },
  },

  watch: {
    modelValue(nVal, oVal) {
      if (nVal != oVal) {
        clearTimeout(this.tId);
        this.tId = setTimeout(() => {
          if (this.modelValue == nVal) {
            this.validateValue();
          }
        }, 500);
      }
    },
  },

  inheritAttrs: false,
  components: { PHInput },
  mixins: [abortController, safeRequest],
};
</script>

<style scoped>
.valid-box {
  @apply relative flex items-center;
}

.result-box {
  @apply absolute right-3 w-5 aspect-square
  rounded-full bg-transparent;
}

.result-box > * {
  @apply block;
}

.valid-disabled .result-box {
  @apply invisible;
}

.result-box.load-anim::after {
  @apply loading-spinner text-primary-light;
}
</style>
