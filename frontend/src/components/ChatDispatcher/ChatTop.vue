<template>
  <div class="chat-top">
    <div class="chat-head">
      <KeepAlive max="2">
        <DynamicComp :key="chatType" :path="currPath" :chat="chat">
          <template #fallback>
            <div class="sk-animate">
              <div
                class="load-sk p-8 rounded-full bg-base-content/30 animate-pulse aspect-square"
              ></div>
              <div class="col-flex items-start">
                <div class="load-sk p-2 min-w-[350px] rounded-full"></div>
                <div class="load-sk p-2 min-w-[180px] rounded-full"></div>
              </div>
            </div>
          </template>
        </DynamicComp>
      </KeepAlive>
      <div>
        <button
          @click="$emit('update:showSide', !showSide)"
          class="icon-btn py-2.5 px-3 opacity-60 hover:opacity-100"
        >
          <i
            v-if="!showSide"
            class="bi bi-layout-sidebar-inset-reverse py-0.5"
          ></i>
          <i v-else class="fa-solid fa-xmark"></i>
        </button>
      </div>
    </div>
    <TracksPlayer v-if="$tracks.files.length" />
  </div>
</template>

<script>
import TracksPlayer from "@/components/Media/List/TracksPlayer.vue";

import dispatchMixin from "./dispatchMixin";

export default {
  props: {
    showSide: {
      type: Boolean,
      required: true,
    },
  },

  _compPaths: {
    chat: "Chat/ChatTop.vue",
    group: "Group/GroupTop.vue",
  },

  mixins: [dispatchMixin],

  components: { TracksPlayer },
  emits: ["update:showSide"],
};
</script>

<style scoped>
.sk-animate {
  @apply flex items-center gap-2;
}

.chat-top {
  @apply sticky top-0 pointer-events-none
  z-[10] shrink-0;
}

.chat-head {
  @apply border-b border-base-content/10 pointer-events-auto;
}

.chat-head {
  @apply flex items-center px-4 py-1 justify-between
 bg-base-200/80 backdrop-blur-xl;
}
</style>
