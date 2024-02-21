<template>
  <div class="shrink-0 bg-base-300 p-2 rounded-xl">
    <div class="tabs-box">
      <div
        v-for="tab in tabs"
        :class="{ 'active-tab': modelValue == tab }"
        @click="(e) => selected(e, tab)"
      >
        <slot :tab="tab">
          {{ tab }}
        </slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    tabs: {
      type: Array,
      required: true,
    },
    modelValue: {
      required: true,
    },
  },

  methods: {
    selected({ target }, tab) {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
        inline: "center",
      });
      if (this.modelValue != tab) {
        this.$emit("update:modelValue", tab);
      }
    },
  },

  emits: ["update:modelValue"],
};
</script>

<style scoped>
.tabs-box {
  --min-size: 120px;
  @apply flex gap-2 items-center justify-start
   overflow-hidden overflow-x-auto;
}

@supports not selector(::-webkit-scrollbar) {
  .tabs-box {
    scrollbar-width: none;
  }
}

.tabs-box::-webkit-scrollbar {
  @apply hidden;
}

.tabs-box > * {
  @apply flex-1
  min-w-[--min-size] transition-transform
  active:scale-95
  text-center cursor-pointer 
  py-2 rounded-xl opacity-60 capitalize;
}

.tabs-box > *:not(.active-tab) {
  @apply bg-base-100 hover:opacity-100;
}

.active-tab {
  @apply opacity-100 bg-primary-medium text-white;
}
</style>
