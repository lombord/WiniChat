<template>
  <Collapse class="collapse-box">
    <span class="text-3xl opacity-70"><i :class="iconCls"></i></span>
    <div class="flex-1">
      <p class="opacity-70 capitalize">{{ title }}</p>
      <div class="break-words break-all">
        <slot />
      </div>
    </div>
  </Collapse>
</template>

<script>
import Collapse from "./Collapse.vue";
export default {
  props: {
    iconCls: {
      type: String,
      default: "fa-solid fa-circle-exclamation",
    },
    title: {
      type: String,
      default: "Info",
    },
  },
  components: { Collapse },
};
</script>

<style scoped>
.collapse-box {
  @apply flex gap-2 items-start shrink-0;
}
</style>
