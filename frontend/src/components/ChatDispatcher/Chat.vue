<template>
  <KeepAlive :max="3">
    <DynamicComp
      :path="currPath"
      v-bind="$attrs"
      :chat="chat"
      :key="getKey(chat)"
    >
      <template #fallback>
        <div class="flex-1 col-flex gap-0">
          <div class="col-flex gap-2 p-3 flex-1">
            <div
              v-for="i in 10"
              class="col-flex"
              :class="{ 'items-end': !(i % 2) }"
            >
              <div class="load-sk p-4 rounded-full w-[300px]"></div>
              <div class="load-sk p-4 rounded-full w-[200px]"></div>
              <div class="load-sk p-4 rounded-full w-[100px]"></div>
            </div>
          </div>
          <div class="flex p-3 bg-base-200 sticky bottom-0">
            <div
              class="load-sk p-6 rounded-xl flex-1 max-w-[600px] mx-auto"
            ></div>
          </div>
        </div>
      </template>
    </DynamicComp>
  </KeepAlive>
</template>

<script>
import dispatchMixin from "./dispatchMixin";

export default {
  expose: ["scrolled"],
  _compPaths: {
    chat: "Chat/Chat.vue",
    group: "Group/GroupChat.vue",
  },

  mixins: [dispatchMixin],
  inheritAttrs: false,
};
</script>

<style scoped></style>
