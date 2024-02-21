<template>
  <Modal v-model:show="iShow" class="p-0">
    <InvitePeople
      class="p-3"
      v-bind="$attrs"
      @accessDenied="iShow = false"
      @invited="passInvited"
    />
  </Modal>
</template>

<script>
import Modal from "@/components/UI/Modal.vue";
import InvitePeople from "./InvitePeople.vue";

export default {
  props: {
    show: {
      type: Boolean,
      required: true,
    },
  },

  computed: {
    iShow: {
      get() {
        return this.show;
      },

      set(val) {
        this.$emit("update:show", val);
      },
    },
  },

  methods: {
    passInvited(...args) {
      this.$emit("invited", ...args);
      this.iShow = false;
    },
  },

  emits: ["invited", "update:show"],
  components: { Modal, InvitePeople },
  inheritAttrs: false,
};
</script>

<style scoped></style>
