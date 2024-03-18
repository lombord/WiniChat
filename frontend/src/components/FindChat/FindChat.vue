<template>
  <Modal class="root-box col-flex">
    <Search v-model="query" />

    <FetchObserver ref="fetchElm" class="overflow-y-auto min-h-[130px]">
      <QDispatch
        v-if="dataList.length"
        @pChosen="postChat"
        @gChosen="joinGroup"
        :qResult="dataList"
      />
      <div v-else class="min-h-[inherit] center-content">
        <h2 class="text-secondary text-center">
          <i class="bi bi-person-fill-x"></i>
        </h2>
      </div>
    </FetchObserver>
  </Modal>
</template>

<script>
import Modal from "@/components/UI/Modal.vue";
import Search from "@/components/Forms/Widgets/Search.vue";
import fetchData from "@/mixins/fetchData.js";
import startChat from "@/components/Chat/startChat.js";

import QDispatch from "./QDispatch.vue";

export default {
  data: () => ({
    query: "",
  }),

  props: {
    chats: {
      type: Map,
      required: true,
    },
  },

  computed: {
    fetchUrl() {
      return `search/?q=${this.query}`;
    },
  },

  methods: {
    async processProm(prom, elm) {
      try {
        return await this.$session.animate(prom, elm);
      } catch (err) {
        this.$flashes.axiosError(err);
        throw err;
      } finally {
        elm.setAttribute("disabled", "disabled");
      }
    },

    postChat({ id: to_user }, elm) {
      const prom = this.startChat(to_user);
      this.processProm(prom, elm);
    },

    async joinGroup(url, elm) {
      const prom = this.$session.put(url);
      try {
        const {
          data: { group, member },
        } = await this.processProm(prom, elm);
        this.$chats.add(group);
        this.$session.socket.sendGroupEvent({
          event: "join",
          group_id: group.id,
          member: member,
        });
      } catch (err) {
        console.log(err);
      }
    },
  },

  watch: {
    query() {
      this.fetchData();
    },
  },

  mixins: [fetchData, startChat],
  components: { Modal, Search, QDispatch },
};
</script>

<style scoped>
.root-box {
  @apply gap-4;
}

.observer {
  @apply py-4 mt-2 after:loading-spinner;
}
</style>
