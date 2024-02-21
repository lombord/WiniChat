<template>
  <GroupTab class="overflow-y-auto p-0" boxCls="gap-0">
    <template #header>
      <span>
        <i class="fa-solid fa-pen-to-square"></i>
      </span>
      <span>Edit Group</span>
    </template>
    <template #content>
      <GroupForm
        ref="groupForm"
        :config="editCfg"
        :group="group"
        :disabled="!editing"
        :getPromElm="() => $refs.saveBtn"
        :isEditForm="true"
        successMessage="Changes have been saved"
        @succeed="groupUpdated"
      >
        <template #submitBtn>
          <div class="col-flex mt-2">
            <template v-if="!editing">
              <button
                @click="editing = true"
                type="button"
                class="w-btn btn-primary"
              >
                <span><i class="fa-solid fa-pen"></i></span>
                <span>Edit</span>
              </button>
            </template>
            <template v-else>
              <button
                ref="saveBtn"
                type="submit"
                class="w-btn btn-primary spinner-on-load"
              >
                <span><i class="fa-solid fa-check"></i></span>
                <span>Save</span>
              </button>
              <button @click="cancelEdit" type="button" class="w-btn btn-error">
                <span><i class="fa-solid fa-ban"></i></span>
                <span>Cancel</span>
              </button>
            </template>
          </div>
        </template>
      </GroupForm>
    </template>
  </GroupTab>
</template>

<script>
import GroupTab from "../GroupSettings/GroupTab.vue";
import GroupForm from "../GroupForm";
import accessRequired from "../GroupRoles/accessRequired.js";

export default {
  name: "EditGroup",

  data: () => ({
    editing: false,
    accessPerm: "edit_group",
  }),

  props: {
    group: {
      type: Object,
      required: true,
    },
  },

  computed: {
    role() {
      return this.group.user_role;
    },
    editCfg() {
      return {
        method: "patch",
        url: this.group.url,
      };
    },
  },

  methods: {
    cancelEdit() {
      this.editing = false;
      this.$refs.groupForm.setInitial();
    },

    groupUpdated({ data }) {
      const { group } = this;
      Object.assign(group, data);
      this.$session.socket.sendGroupEvent({
        event: "update",
        group_id: group.id,
        data,
      });
      this.editing = false;
      this.$emit("close");
    },
  },

  components: { GroupTab, GroupForm },
  mixins: [accessRequired],
};
</script>

<style scoped></style>
