<template>
  <div @mouseup.stop.prevent class="root" v-if="show">
    <div class="buttons" v-for="(item, i) in menu" :key="i">
      <button
        @click="selected(item)"
        class="menu-btn"
        :contextId="[item.label]"
      >
        <slot :name="item.label">
          {{ item.label }}
        </slot>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  expose: ["$el"],
  props: {
    menu: {
      type: Array,
      required: true,
    },
    show: {
      type: Boolean,
      required: true,
    },
  },

  updated() {
    document.addEventListener(
      "mouseup",
      () => this.$emit("update:show", false),
      { once: true }
    );
  },

  methods: {
    selected(item) {
      this.$emit("update:show", false);
      item.cb && item.cb();
      this.$nextTick(() => this.$emit("chosen"));
    },
  },
};
</script>

<style scoped>
.root {
  @apply absolute p-2.5 bg-base-300/20 
  rounded-xl overflow-hidden 
  flex flex-col gap-2 shadow
  z-50 backdrop-blur-xl;
}

.menu-btn {
  @apply btn bg-base-100/50 
  border-base-content/[10%] w-full py-4;
}
</style>
