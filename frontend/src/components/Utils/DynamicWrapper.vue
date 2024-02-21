<template>
  <div>
    <DynamicComp v-bind="$attrs">
      <template v-for="(_, slot) in $slots" v-slot:[slot]="scope">
        <slot :name="slot" v-bind="scope" />
      </template>
    </DynamicComp>
  </div>
</template>

<script>
import DynamicComp from "./DynamicComp.vue";
export default {
  props: {
    rootCls: {
      type: String,
      default: "",
    },
  },
  components: { DynamicComp },
  inheritAttrs: false,
};
</script>

<style scoped></style>
