<template>
  <div class="py-2 flex flex-col-reverse">
    <slot name="top"></slot>
    <div
      v-for="(messages, date) in msgGroup"
      :key="date"
      class="messages gap-2"
    >
      <template v-for="(context, i) in messages" :key="i">
        <div
          v-for="{ isSession, owner } in [getTmpObj(context[0])]"
          :class="{ 'context-start': !isSession }"
          class="msg-context"
        >
          <div class="messages flex-1">
            <Message
              :class="isSession ? 'chat-end' : 'chat-start'"
              v-for="(msg, i) in context"
              :key="msg.id || i"
              :message="msg"
              :isSession="isSession"
              :owner="owner"
              v-bind="$attrs"
            />
          </div>
          <div class="chat-image avatar sticky bottom-[4.5rem]">
            <div class="round-img owner-avatar w-12">
              <img :src="owner.photo" class="w-full" />
            </div>
          </div>
        </div>
      </template>
      <div class="date-divider" :class="{ 'player-divider': isPlayerVisible }">
        <span class="date-badge badge badge-primary">
          {{ divDate(date) }}
        </span>
      </div>
    </div>
    <slot name="bottom"></slot>
  </div>
</template>

<script>
import Message from "./Message.vue";
import moment from "moment";

export default {
  props: {
    messages: {
      type: Array,
      required: true,
    },
    companion: {
      type: Object,
      required: true,
    },
    user: {
      type: Object,
      required: true,
    },
  },

  computed: {
    msgGroup() {
      let result = {};
      this.messages.forEach((msg) => {
        let created = moment(msg.created).format("YYYY-MM-DD");
        const messages = result[created] || (result[created] = [[]]);
        const context = messages.at(-1);
        if (this.isEndContext(msg, context.at(-1))) messages.push([msg]);
        else context.push(msg);
      });
      return result;
    },
    isPlayerVisible() {
      return !!this.$tracks.component;
    },
  },

  methods: {
    getOwner(msg) {
      if (msg.owner === undefined) return this.user;
      return msg.owner == this.user.id ? this.user : this.companion;
    },

    checkSession(msg) {
      try {
        return msg.owner === undefined || this.$session.user.id === msg.owner;
      } catch (err) {}
    },

    getTmpObj(msg) {
      return {
        isSession: this.checkSession(msg),
        owner: this.getOwner(msg),
      };
    },

    divDate(date) {
      return moment(date).calendar(null, {
        sameDay: "[Today]",
        nextWeek: "dddd",
        lastDay: "[Yesterday]",
        lastWeek: "dddd",
        sameElse: "DD/MM/YYYY",
      });
    },

    isEndContext(msg1, msg2) {
      msg1.owner || (msg1.owner = this.user.id);
      try {
        return msg1.owner !== msg2.owner;
      } catch (err) {
        return false;
      }
    },
  },

  inheritAttrs: false,

  components: { Message },
};
</script>

<style scoped>
.messages {
  @apply flex flex-col-reverse gap-0.5;
}

.msg-context {
  @apply flex items-end;
}
.context-start {
  @apply flex-row-reverse;
}

.msg-context .messages > *:not(:first-child):deep(.chat-bubble) {
  @apply before:content-[0];
}

.msg-context :deep(.chat-end .chat-bubble) {
  @apply chat-bubble-primary rounded-r-lg;
}

.msg-context :deep(.chat-start .chat-bubble) {
  @apply chat-bubble-secondary rounded-l-lg;
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

.date-divider {
  @apply text-center pointer-events-none sticky top-20 lg:top-24 z-10 py-2;
}

.player-divider {
  @apply top-32;
}

.date-badge {
  @apply text-base p-3 
  bg-opacity-60 text-white border-none
  drop-shadow;
}
</style>
