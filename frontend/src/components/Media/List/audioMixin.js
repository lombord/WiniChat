import moment from "moment";
import fileMixin from "@/mixins/fileMixin.js";

export default {
  computed: {
    title() {
      return this.metadata.title || this.metadata.file_name;
    },
    author() {
      return this.metadata.author || "Unknown";
    },
    duration() {
      return this.metadata.duration;
    },
    durationFormat() {
      const durMom = moment.utc(this.duration * 1000);
      const FT = durMom.hour() >= 1 ? "h:mm:ss" : "m:ss";
      return durMom.format(FT);
    },
  },
  mixins: [fileMixin],
};
