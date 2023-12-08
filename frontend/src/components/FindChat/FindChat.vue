<template>
  <Modal class="root-box col-flex">
    <Search v-model="query" />
    <div ref="fetchElm" class="overflow-y-auto flex-1 pr-1 relative">
      <QPeople @chosen="startChat" v-if="dataList.length" :people="dataList">
        <template #bottom>
          <div v-int="loadNext" class="pt-20">

            <div :key="query || 0" class="load-anim observer"></div>
          </div>
        </template>
      </QPeople>
      <div v-else class="absolute inset-0 center-content">
        <h4  class="text-primary text-center">Empty</h4>
      </div>
    </div>
  </Modal>
</template>

<script>
import Modal from "@/components/UI/Modal.vue";
import Search from "@/components/forms/Search.vue";

import fetchData from "@/mixins/fetchData";

import QPeople from "./QPeople.vue";

export default {
  data: () => ({
    query: "",
  }),

  props: {
    chats: {
      type: Array,
      required: true,
    },
  },

  computed: {
    url() {
      return `people/?qr=${this.query}`;
    },
  },

  methods: {
    async startChat({ id: to_user }, elm) {
      const prom = this.$session.post("chats/", { to_user });
      try {
        const { data } = await this.$session.animate(prom, elm);
        const { id: chat_id } = data;
        this.$session.socket.sendEvent("new_chat", { chat_id });
        this.chats.unshift(data);
      } catch ({ response: { data } }) {
        this.$flashes.error(data["__all__"][0]);
      }
      elm.setAttribute("disabled", "disabled");
    },
  },

  watch: {
    query() {
      if (this.controller) {
        this.controller.abort();
      }
      this.fetchData();
    },
  },

  mixins: [fetchData],
  components: { Modal, Search, QPeople },
};
</script>

<style scoped>
.root-box {
  @apply gap-4;
}

.observer {
  @apply py-4 mt-2 after:w-[30px] after:loading-spinner;
}
</style>
