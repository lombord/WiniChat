import moment from "moment";

export default {
  props: {
    chat: {
      type: Object,
      required: true,
    },
  },

  computed: {
    latest() {
      return this.chat.latest;
    },

    isSession() {
      return this.latest.owner == this.$session.user.id;
    },

    unread() {
      return this.chat.unread;
    },

    created() {
      const data = moment(this.latest.created);
      return data.calendar(null, {
        sameDay: "LT",
        nextWeek: "ddd",
        lastDay: "[Yester.]",
        lastWeek: "ddd",
        sameElse: "DD/MM/YYYY",
      });
    },
  },
};
