import MediaSlide from "./MediaSlide.vue";

export default {
  data: () => ({
    currIdx: 0,
    show: false,
  }),

  props: {
    files: {
      type: Array,
      required: true,
    },
  },

  methods: {
    showSlide(i) {
      this.currIdx = i;
      this.show = true;
    },
  },

  components: { MediaSlide },
};
