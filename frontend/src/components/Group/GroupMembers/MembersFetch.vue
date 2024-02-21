<template>
  <FetchObserver :hasBottom="!!next" :fetchBottom="fetchNext">
    <Members v-if="loaded" :members="sortedMembers" :group="group" />
  </FetchObserver>
</template>

<script>
import fetchData from "@/mixins/fetchData.js";
import Members from "./Members.vue";
import trackMembers from "./trackMembers.js";

export default {
  data: () => ({
    limit: 30,
  }),

  methods: {
    firstAdd(data) {
      this.initMembers(data);
    },

    addNext(data) {
      this.addMembers(data);
    },
  },

  components: { Members },
  mixins: [fetchData, trackMembers],
};
</script>

<style scoped></style>
