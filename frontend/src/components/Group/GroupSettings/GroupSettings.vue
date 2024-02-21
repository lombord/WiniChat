<template>
  <Modal class="root-box p-0 min-h-[400px]">
    <DynamicComps
      excludeCP="GroupInvite,"
      v-model:current="current"
      :comps="gComponents"
    >
      <template #fallback>
        <div class="settings-box">
          <ImgOverlay class="rounded-2xl" :url="group.photo">
            <h6 class="text-white/95 text-2xl">
              {{ group.name }}
            </h6>
            <div class="flex gap-2 items-center">
              <p class="text-white/70 flex text-base font-bold gap-0.5">
                <span class="text-primary-light">
                  <i class="fa-solid fa-user-group"></i>
                </span>
                {{ group.members }}
              </p>
              <p class="text-white/70 flex text-base font-bold gap-0.5">
                <span class="text-success">
                  <i class="fa-solid fa-circle"></i>
                </span>
                {{ group.online }}
              </p>
            </div>
          </ImgOverlay>
          <GridButtons :options="gOptions" @chosen="changeCurrent" />
        </div>
      </template>
      <template #membersFB>
        <div class="p-2 flex col-flex gap-2">
          <div class="p-7 load-sk rounded-full overflow-hidden max-h-fit"></div>
          <ListSkeleton :count="7">
            <div class="flex gap-2 items-center">
              <div class="p-7 aspect-square rounded-full load-sk"></div>
              <div class="flex-1 col-flex">
                <div class="p-2 max-w-[200px] rounded-full load-sk"></div>
                <div class="p-2 max-w-[100px] rounded-full load-sk"></div>
              </div>
            </div>
          </ListSkeleton>
        </div>
      </template>
    </DynamicComps>
  </Modal>
</template>

<script>
import { computed } from "vue";
import Modal from "@/components/UI/Modal.vue";
import ImgOverlay from "@/components/Media/Images/ImgOverlay.vue";
import GridButtons from "@/components/UI/GridButtons/GridButtons.vue";
import DynamicComps from "@/components/Utils/DynamicComps.vue";
import ListSkeleton from "@/components/Skeletons/ListSkeleton.vue";
import permission from "../GroupRoles/permission.js";
import commonActions from "../commonActions.js";

export default {
  data: () => ({
    current: null,
    gOptions: null,
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

    gComponents() {
      const { group } = this;
      return {
        members: {
          path: "Group/GroupMembers",
          attrs: { group },
        },
        roles: {
          path: "Group/GroupRoles",
          attrs: { group },
        },
        bans: {
          path: "Group/GroupBans",
          attrs: { group },
        },
        invite: {
          path: "Group/GroupInvite",
          attrs: { group },
        },
        info: {
          path: "Group/GroupDetails",
          attrs: { group },
        },
      };
    },
  },

  created() {
    this.gOptions = [
      {
        label: "Members",
        icon: "fa-solid fa-user-group",
      },
      {
        label: "Roles",
        icon: "fa-solid fa-shield-halved",
      },
      {
        label: "Bans",
        icon: "fa-solid fa-user-lock",
        hidden: computed(() => !this.hasPerm("unban_user")),
      },
      {
        label: "Invite",
        icon: "fa-solid fa-user-plus",
        hidden: computed(() => !this.canAdd),
      },
      {
        label: "Info",
        icon: "fa-solid fa-circle-info",
      },
      {
        label: "Leave",
        icon: "fa-solid fa-arrow-right-from-bracket",
        cls: "error-grid-btn",
        cb: this.leaveGroup,
        hidden: computed(() => this.isOwner),
      },
      {
        label: "Delete",
        icon: "fa-solid fa-trash",
        cls: "error-grid-btn",
        cb: this.deleteGroup,
        hidden: computed(() => !this.isOwner),
      },
    ];
  },

  methods: {
    changeCurrent(value) {
      this.current = value;
    },

    async deleteGroup() {
      if (!this.isOwner) return;
      const session = this.$session;
      const { group } = this;
      let data = null;
      try {
        ({ data } = await session.delete(group.url));
      } catch (error) {
        this.$flashes.axiosError(error);
      }
      session.socket.sendGroupEvent({
        event: "deleted",
        group_id: group.id,
        people: data,
      });
      this.$chats.removeChat(group);
    },
  },

  components: { Modal, ImgOverlay, GridButtons, DynamicComps, ListSkeleton },
  mixins: [permission, commonActions],
};
</script>

<style scoped>
.settings-box {
  @apply p-3 flex flex-col gap-3 overflow-y-auto max-h-[inherit];
}

:deep(.sk-item) {
  @apply bg-base-300;
}

:deep(.error-grid-btn) {
  --active-color: theme(colors.error);
  --font-color: theme(colors.error);
  @apply text-error;
}
</style>
