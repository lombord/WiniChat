<template>
  <div @mouseup.stop.prevent class="root" v-if="show">
    <div class="buttons" v-for="(item, i) in menu" :key="i">
      <button
        @click="selected(item)"
        class="menu-btn btn"
        :class="item.cls"
        :contextId="[item.label]"
      >
        <slot :name="item.label">
          <span><i :class="item.icon || 'fa-solid fa-circle'"></i></span>
          <span>
            {{ item.label }}
          </span>
        </slot>
      </button>
    </div>
  </div>
</template>

<script>
import context from "./context.js";

export default {
  expose: ["$el"],

  mixins: [context],
};
</script>

<style scoped>
.root {
  @apply absolute p-1.5 bg-base-300/50 
  rounded-2xl overflow-hidden backdrop-blur-xl
  flex flex-col gap-1.5 shadow-md z-50;
  transform: translate3d(0, 0, 0);
  backface-visibility: hidden;
}

.menu-btn {
  @apply bg-base-100/50
  flex justify-center items-center
  text-base-content/90 px-3
  outline outline-1 rounded-2xl
  outline-base-content/[15%] 
  border-none w-full py-3.5;
  transform: translate3d(0, 0, 0);
  backface-visibility: hidden;
}

.menu-btn:is(:hover) {
  @apply text-white/90 outline-transparent
  bg-primary-light shadow-md;
}

.menu-btn:hover :is(*, :deep(*)) {
  @apply text-white/90 !important;
}
</style>
