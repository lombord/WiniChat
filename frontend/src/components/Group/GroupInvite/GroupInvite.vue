<template>
  <GroupTab @close="closeTab">
    <template #header>
      <span>
        <i class="fa-solid fa-user-plus"></i>
      </span>
      <span class="max-[475px]:hidden">Invite</span>
    </template>
    <template #content>
      <InvitePeople
        :group="group"
        @accessDenied="closeTab"
        @invited="closeTab"
      />
    </template>
  </GroupTab>
</template>

<script>
import GroupTab from "../GroupSettings/GroupTab.vue";
import InvitePeople from "./InvitePeople.vue";

export default {
  name: "GroupInvite",
  props: {
    group: {
      type: Object,
      required: true,
    },
  },

  methods: {
    closeTab() {
      this.$emit("close");
    },
  },

  components: { GroupTab, InvitePeople },
  emits: ["close"],
};
</script>

<style scoped></style>
