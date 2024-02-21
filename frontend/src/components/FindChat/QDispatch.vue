<template>
  <div class="result-box col-flex gap-1.5">
    <component
      v-for="qItem in qResult"
      :is="comps[qItem.type]"
      :key="`${qItem.type}:${qItem.id}`"
      :qItem="qItem"
      v-bind="$attrs"
    />
  </div>
</template>

<script>
import QPerson from "./QPerson.vue";
import QGroup from "./QGroup.vue";

export default {
  props: {
    qResult: {
      type: Array,
      required: true,
    },
  },

  computed: {
    comps() {
      return {
        group: "QGroup",
        user: "QPerson",
      };
    },
  },

  inheritAttrs: false,
  components: { QPerson, QGroup },
};
</script>

<style scoped>
.result-box > * {
  @apply p-2 pr-3 bg-base-300/60
  cursor-pointer flex items-center gap-2
  rounded-2xl active:scale-[0.97] transition
  hover:bg-base-content/15;
}
</style>
