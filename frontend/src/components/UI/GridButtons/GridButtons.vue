<template>
  <div :class="$attrs.class" class="dynamic-grid options-box">
    <TransitionGroup name="pop">
      <template v-for="(option, i) in options" :key="option.label || i">
        <GridButton
          v-if="!option.hidden"
          v-bind="getListeners()"
          :option="option"
        />
      </template>
    </TransitionGroup>
  </div>
</template>

<script>
import GridButton from "./GridButton.vue";

export default {
  props: {
    options: {
      type: Array,
      required: true,
    },
  },

  methods: {
    getListeners() {
      const pattern = /^on[A-Z]\w+$/;
      const filtered = Object.entries(this.$attrs).filter(([key]) =>
        pattern.test(key)
      );
      return Object.fromEntries(filtered);
    },
  },

  inheritAttrs: false,
  components: { GridButton },
};
</script>

<style scoped>
.options-box {
  --min-size: 150px;
}
</style>
