export default {
  props: {
    file: {
      type: Object,
      required: true,
    },
  },
  computed: {
    url() {
      return this.file.url;
    },
    metadata() {
      return this.file.metadata;
    },

    file_size() {
      return this.$utils.formatBytes(this.metadata.size);
    },

    file_name() {
      return this.metadata.file_name || this.url.split("/").reverse()[0];
    },
  },
  methods: {},
};
