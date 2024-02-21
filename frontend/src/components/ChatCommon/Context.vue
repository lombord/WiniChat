<template>
  <div :class="{ 'context-start': !isSession }" class="msg-context">
    <div class="messages flex-1">
      <TransitionGroup name="message">
        <Message
          :class="isSession ? 'chat-end' : 'chat-start'"
          class="relative"
          @contextmenu.stop.prevent="(e) => toggleContext(msg, e)"
          v-for="msg in messages"
          :key="msg.uuid || msg.id"
          :message="msg"
          :isSession="isSession"
          :owner="owner"
          v-bind="$attrs"
        />
      </TransitionGroup>
    </div>
    <ContextManager
      ref="context"
      v-model:show="showCtx"
      class="msg-context-menu"
      :menu="contextMenu"
      :extraArgs="[currentMsg]"
    />
    <div class="chat-image avatar sticky bottom-[4.5rem]">
      <div
        @click="$profile.show(owner.id)"
        class="round-img cursor-pointer owner-avatar w-12 shadow"
      >
        <ImgAnim :src="owner.photo" class="w-full" />
      </div>
    </div>
  </div>
</template>

<script>
import Message from "./Message.vue";
import ContextManager from "@/components/Utils/ContextManager.vue";
import trackUser from "@/components/User/trackUser.js";

export default {
  data: () => ({
    wsFetch: true,
    contextMenu: null,
    currentMsg: null,
    currElm: null,
    showCtx: false,
  }),

  props: {
    messages: {
      type: Array,
      required: true,
    },

    owner: {
      type: Object,
      required: true,
    },

    getContextMenu: {
      type: Function,
      required: true,
    },
  },

  computed: {
    isSession() {
      return this.owner.id == this.$session.user.id;
    },

    user() {
      return this.owner;
    },

    userId() {
      return this.owner.id;
    },

    showContext() {
      return this.$refs.context.showContext;
    },
  },

  created() {
    this.contextMenu = this.getContextMenu(this.owner);
  },

  methods: {
    toggleContext(msg, evt) {
      this.currentMsg = msg;
      this.currElm = evt.currentTarget;
      this.showContext(evt);
    },
  },

  inheritAttrs: false,
  components: { Message, ContextManager },
  mixins: [trackUser],
};
</script>

<style scoped>
.msg-context {
  @apply flex items-end;
}

.context-start {
  @apply flex-row-reverse;
}

.msg-context-menu {
  @apply max-w-[160px] origin-top-left;
}

.owner-enter-active,
.owner-leave-active {
  @apply transition;
}

.owner-enter-from,
.owner-leave-to {
  @apply opacity-0;
}

.chat-image {
  @apply transition-all outline-primary 
  z-10 outline outline-0 rounded-full;
  filter: blur(0);
  transform: translateZ(0);
  backface-visibility: hidden;
}

.chat-image:hover {
  @apply outline-[3px] 
  outline-primary-medium outline-offset-2;
}

.chat-image:hover:active {
  @apply outline-offset-4 outline-primary-light;
  transform: translateZ(0) scale(0.95);
}

.messages {
  @apply flex flex-col-reverse gap-0.5;
}

.active-context {
  @apply bg-base-100/80 relative;
}

.msg-context .messages > *:not(:first-child):deep(.chat-bubble) {
  @apply before:content-[0];
}

.msg-context :deep(.chat-end .chat-bubble) {
  @apply bg-primary-medium text-white rounded-r-lg;
}

.msg-context :deep(.chat-start .chat-bubble) {
  @apply chat-bubble-accent text-white/90 rounded-l-lg;
}

.msg-context .messages > *:last-child:deep(.chat-start .chat-bubble) {
  @apply rounded-tl-3xl;
}
.msg-context
  .messages
  > *:not(:first-child):last-child:deep(.chat-end .chat-bubble) {
  @apply rounded-tr-3xl;
}

.msg-context .messages > *:first-child:deep(.chat-start .chat-bubble) {
  @apply rounded-bl-none;
}
.msg-context .messages > *:first-child:deep(.chat-end .chat-bubble) {
  @apply rounded-br-none;
}

.msg-context .messages > *:first-child:last-child:deep(.chat-bubble) {
  @apply rounded-t-box;
}

.message-enter-active,
.message-leave-active {
  /* transition: opacity 0.5s ease; */
  @apply transition;
}

.message-enter-from,
.message-leave-to {
  @apply opacity-0;
}

.message-enter-from {
  transform: translateY(30px);
}

.message-leave-to:has(.chat-end) {
  transform: translateX(30px);
}

.message-leave-to:has(.chat-start) {
  transform: translateX(-30px);
}
</style>
