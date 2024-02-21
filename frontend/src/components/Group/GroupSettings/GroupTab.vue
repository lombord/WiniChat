<template>
  <div
    class="max-h-[inherit] min-h-[inherit] overflow-hidden col-flex"
    :class="boxCls"
  >
    <div class="tab-header">
      <h4 class="text-primary-light flex gap-1 items-center">
        <slot name="header" />
      </h4>
      <slot name="goBack">
        <button class="icon-btn back-btn" @click="$emit('close')">
          <i class="fa-solid fa-arrow-left"></i>
        </button>
      </slot>
    </div>
    <div class="tab-content" :class="$attrs.class">
      <slot name="content" />
    </div>
    <slot name="bottom" />
  </div>
</template>

<script>
export default {
  props: {
    boxCls: {
      type: String,
      default: "",
    },
  },

  emits: ["close"],
  inheritAttrs: false,
};
</script>

<style scoped>
.tab-header {
  @apply flex items-center bg-base-200 border-b 
  border-base-content/10 justify-center relative p-3;
}

.back-btn {
  @apply text-base-content/40 hover:text-base-content/80
  absolute left-3 p-2 text-3xl;
}

.tab-content {
  @apply flex-1 px-2 pb-2 flex flex-col gap-2 overflow-hidden;
}
</style>
