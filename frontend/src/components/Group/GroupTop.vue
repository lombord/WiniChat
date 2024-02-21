<template>
  <div class="top-box" @click="showST = true">
    <div class="round-img w-16 overflow-hidden border border-base-content/[5%]">
      <ImgAnim :src="chat.photo" class="full-img" />
    </div>
    <div>
      <h5 class="text-primary-light">{{ chat.name }}</h5>
      <div class="flex gap-1 text-base-content/80">
        <p>{{ chat.members }} members,</p>
        <p>{{ chat.online }} online</p>
      </div>
    </div>
  </div>
  <GroupSettings v-if="showST" :group="chat" v-model:show="showST" />
</template>

<script>
import GroupSettings from "./GroupSettings";

export default {
  props: {
    chat: {
      type: Object,
      required: true,
    },
  },

  computed: {
    showST: {
      get() {
        return this.$group.showSettings;
      },
      set(val) {
        this.$group.showSettings = val;
      },
    },
  },

  deactivated() {
    this.showST = false;
  },

  components: { GroupSettings },
};
</script>

<style scoped>
.top-box {
  @apply flex items-center gap-2 
  truncate cursor-pointer;
}
</style>
