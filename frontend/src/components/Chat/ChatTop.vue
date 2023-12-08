<template>
  <div class="chat-top">
    <div class="chat-head">
      <div class="user-short">
        <div class="avatar" :class="avatarCls">
          <div class="round-img w-16">
            <img :src="companion.photo" />
          </div>
        </div>
        <h5 class="text-primary">{{ username }}</h5>
      </div>
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
export default {
  props: {
    companion: {
      type: Object,
      required: true,
    },
    showSide: {
      type: Boolean,
      required: true,
    },
  },

  computed: {
    username() {
      return this.companion.full_name || this.companion.username;
    },
    avatarCls() {
      return this.companion.status ? "online" : "offline";
    },
  },

  components: { TracksPlayer },
  emits: ["update:showSide"],
};
</script>

<style scoped>
.chat-top {
  @apply sticky top-0 pointer-events-none
  z-[10] shrink-0;
}

.chat-head {
  @apply border-b border-base-content/10 pointer-events-auto;
}

.chat-head {
  @apply flex items-center px-4 py-1 justify-between
 bg-base-200/50 backdrop-blur-3xl;
}

.user-short {
  @apply flex gap-2 items-center truncate;
}
</style>
