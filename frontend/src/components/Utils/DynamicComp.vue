<template>
  <Suspense @resolve="$emit('loaded')" :timeout="5e4">
    <component :is="comp" v-bind="$attrs" />
    <template #fallback>
      <slot name="fallback">
        <div :class="$attrs.class" class="load-anim fallback-load"></div>
      </slot>
    </template>
  </Suspense>
</template>

<script>
export default {
  name: "DynamicComp",

  props: {
    path: {
      type: String,
      required: true,
    },
  },

  computed: {
    comp() {
      return this.$utils.dynImport(this.path);
    },
  },

  emits: ["loaded"],
  inheritAttrs: false,
};
</script>

<style scoped></style>
