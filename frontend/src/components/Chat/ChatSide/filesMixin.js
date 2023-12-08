import fetchData from "@/mixins/fetchData.js";

export default {
  props: {
    url: {
      type: String,
      required: true,
    },
  },

  computed: {
    files() {
      return this.dataList;
    },
  },

  mixins: [fetchData],
};
