<template>
  <div class="messages">
    <slot name="top"></slot>
    <div v-for="(msg, i) in messages">
      <Message :key="msg.id || i" :message="msg" :owner="getOwner(msg)" />
    </div>
    <slot name="bottom"></slot>
  </div>
</template>

<script>
import Message from "./Message.vue";

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

  methods: {
    getOwner(msg) {
      if (msg.owner === undefined) return this.user;
      return msg.owner == this.user.id ? this.user : this.companion;
    },
  },

  components: { Message },
};
</script>

<style scoped>
.messages {
  @apply flex flex-col-reverse;
}
</style>
