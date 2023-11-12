<template>
  <div>
    <div class="chat" :class="chatCls">
      <div class="chat-image avatar">
        <div class="round-img">
          <img :src="owner.photo" class="w-12" />
        </div>
      </div>
      <div v-if="isPosted" class="chat-footer">
        <time class="text-xs opacity-50">{{ createdTime }}</time>
      </div>
      <div class="chat-bubble break-words max-w-lg">
        {{ message.content }}
        <span
          v-if="!isPosted"
          class="load-anim align-middle py-1 px-2 ml-2"
        ></span>
      </div>
    </div>
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
    sibling: {
      type: Object,
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
      return moment(this.message.created);
    },

    createdTime() {
      return this.created.format("LT");
    },

    

    siblingDay() {
      return moment(this.sibling.created).day();
    },

    showSep() {
      return !this.sibling || this.created.day() != this.siblingDay;
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
