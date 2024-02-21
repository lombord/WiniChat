<template>
  <Modal v-model:show="iShow" class="p-0">
    <GroupTab class="overflow-y-auto p-0" boxCls="gap-0">
      <template #header>
        <span>
          <i class="fa-solid fa-user-group"></i>
        </span>
        <span>Create Group</span>
      </template>
      <template #goBack>
        <span class="hidden"></span>
      </template>
      <template #content>
        <GroupForm
          submitLabel="Create"
          :isFormData="true"
          :config="requestCfg"
          successMessage="Group has been created"
          @succeed="groupCreated"
        />
      </template>
    </GroupTab>
  </Modal>
</template>

<script>
import Modal from "@/components/UI/Modal.vue";
import GroupTab from "./GroupSettings/GroupTab.vue";
import GroupForm from "./GroupForm";

export default {
  props: {
    show: {
      type: Boolean,
      required: true,
    },
  },

  computed: {
    requestCfg() {
      return {
        url: "groups/",
        method: "POST",
      };
    },

    iShow: {
      get() {
        return this.show;
      },
      set(value) {
        this.$emit("update:show", value);
      },
    },
  },

  methods: {
    groupCreated({ data }) {
      this.$session.socket.sendGroupEvent({
        event: "created",
        group_id: data.id,
      });
      this.$chats.addCurrent(data);
      this.iShow = false;
    },
  },

  components: { Modal, GroupForm, GroupTab },
};
</script>

<style scoped></style>
