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
      return this.formatBytes(this.metadata.size);
    },

    file_name() {
      return this.metadata.file_name || this.url.split("/").reverse()[0];
    },
  },
  methods: {
    formatBytes(bytes, decimals = 2) {
      if (!+bytes) return "0B";
      const k = 1024;
      const dm = decimals < 0 ? 0 : decimals;
      const sizes = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))}${sizes[i]}`;
    },
  },
};
