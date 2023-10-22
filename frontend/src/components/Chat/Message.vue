<template>
  <div class="chat" :class="chatCls">
    <div class="chat-image avatar">
      <div class="round-img">
        <img :src="owner.photo" class="w-12" />
      </div>
    </div>
    <div v-if="isPosted" class="chat-footer">
      <time class="text-xs opacity-50">{{ created }}</time>
    </div>
    <div class="chat-bubble break-words max-w-lg">
      {{ message.content }}
      <span v-if="!isPosted" class="load-anim align-middle py-1 px-2 ml-2"></span>
    </div>
    <!-- <div class="chat-footer opacity-50">Delivered</div> -->
  </div>
</template>

<script>
import moment from "moment";

export default {
  props: {
    owner: {
      type: Object,
      required: true,
    },
    message: {
      type: Object,
      required: true,
    },
  },
  computed: {
    isSession() {
      try {
        return this.$session.user.id === this.owner.id;
      } catch (err) {}
    },
    chatCls() {
      return this.isSession ? "chat-end" : "chat-start";
    },
    created() {
      return moment(this.message.created).format("LT");
    },
    isPosted() {
      return this.message.id !== undefined;
    },
  },
};
</script>

<style scoped>
.chat-end .chat-bubble {
  @apply chat-bubble-primary;
}
.chat-start .chat-bubble {
  @apply chat-bubble-secondary;
}

.load-anim::after {
  @apply loading-spinner text-inherit min-w-[20px];
}
</style>
