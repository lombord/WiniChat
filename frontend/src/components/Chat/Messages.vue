<template>
  <div class="py-2 flex flex-col-reverse">
    <slot name="top"></slot>
    <div v-for="(messages, date) in msgGroup" :key="date" class="messages">
      <Message
        :key="msg.id || i"
        v-for="(msg, i) in messages"
        :message="msg"
        :owner="getOwner(msg)"
      />
      <div class="date-divider">
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
        (result[created] || (result[created] = [])).push(msg);
      });
      return result;
    },
  },

  methods: {
    getOwner(msg) {
      if (msg.owner === undefined) return this.user;
      return msg.owner == this.user.id ? this.user : this.companion;
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
  },

  components: { Message },
};
</script>

<style scoped>
.messages {
  @apply flex flex-col-reverse;
}
.date-divider {
  @apply text-center sticky top-20 md:top-24 py-2;
}
.date-badge {
  @apply text-base p-3 
  bg-opacity-60 text-white border-none
  drop-shadow;
}
</style>
