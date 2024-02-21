<template>
  <KeepAlive :max="3">
    <DynamicComp
      :path="currPath"
      class="dy-chat-side"
      v-bind="$attrs"
      v-if="show"
      :key="getKey(chat)"
      :chat="chat"
    >
      <template #fallback>
        <div class="chat-side py-3 p-2 col-flex justify-start gap-3">
          <div class="load-sk p-10 min-h-[280px] rounded-xl"></div>

          <div class="load-sk p-10 min-h-[50px] rounded-xl"></div>
          <div class="tabs-sk">
            <div v-for="i in 3" class="load-sk"></div>
          </div>
          <div class="dynamic-flex flex-sk">
            <div class="load-sk" v-for="i in 5"></div>
          </div>
        </div>
      </template>
    </DynamicComp>
  </KeepAlive>
</template>

<script>
import GridSkeleton from "@/components/Skeletons/GridSkeleton.vue";
import dispatchMixin from "./dispatchMixin";

export default {
  props: {
    show: {
      type: Boolean,
      required: true,
    },
  },

  _compPaths: {
    chat: "Chat/ChatSide.vue",
    group: "Group/GroupSide.vue",
  },

  mixins: [dispatchMixin],
  components: { GridSkeleton },
  inheritAttrs: false,
};
</script>

<style scoped>
.tabs-sk {
  @apply bg-base-300 gap-4 p-2 rounded-xl flex justify-between;
}

.tabs-sk > * {
  @apply p-6 flex-1 rounded-xl;
}

.flex-sk {
  @apply overflow-hidden rounded-xl gap-1;
}

.flex-sk > * {
  @apply p-24 min-h-[250px];
}
</style>
