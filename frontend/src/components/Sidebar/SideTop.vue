<template>
  <div class="side-top">
    <SideUser />
    <div>
      <button class="w-btn find-btn tflex" @click="findShow = true">
        <span class="text-secondary/80 text-xl">
          <i class="fa-solid fa-circle-nodes"></i>
        </span>
        Explore
      </button>
      <FindChat v-if="findShow" :chats="chats" v-model:show="findShow" />
    </div>
  </div>
</template>

<script>
import SideUser from "./SideUser.vue";
import FindChat from "@/components/FindChat";

export default {
  data: () => ({
    findShow: false,
  }),

  props: {
    chats: {
      type: Map,
      required: true,
    },
  },

  components: { SideUser, FindChat },
};
</script>

<style scoped>
.side-top {
  @apply flex flex-col gap-2 px-2 pb-2;
}

.find-btn {
  @apply break-words 
  btn-primary w-full block;
}
</style>
