<template>
  <div>
    <div class="side-top mb-3">
      <div class="group-img-box">
        <div class="more-box">
          <div>
            <button
              @mouseup.stop
              @click.stop="showMore = !showMore"
              class="btn group-more-btn px-5"
            >
              <i class="fa-solid fa-ellipsis-vertical"></i>
            </button>
          </div>
          <div>
            <GlassMenu
              class="more-menu"
              :class="{ 'load-anim': !role }"
              v-model:show="showMore"
              :menu="moreMenu"
            />
          </div>
        </div>
        <ImgView
          class="full-img"
          :file="{ url: group.photo }"
          @imgLoad="(target) => (imgElm = target)"
        />
      </div>
      <ImgCanvas class="img-canvas" v-if="imgElm" :imgElm="imgElm" />
      <div class="side-card-content">
        <div>
          <h6 class="text-2xl text-base-content/90">
            {{ group.name }}
          </h6>
          <div class="group-stats">
            <p>
              <span class="text-accent">
                <i class="fa-solid fa-user-group"></i>
              </span>
              <span>{{ group.members }}</span>
            </p>
            <p>
              <span class="text-success">
                <i class="fa-solid fa-circle"></i>
              </span>
              <span>{{ group.online }}</span>
            </p>
          </div>
        </div>
        <Transition name="pop">
          <button
            v-if="canAdd"
            @click="showInvite"
            class="btn invite-btn spinner-on-load"
          >
            <span>
              <i class="fa-solid fa-user-plus"></i>
            </span>
          </button>
        </Transition>
        <InviteModal
          v-if="canAdd && iShow"
          v-model:show="iShow"
          :group="group"
        />
      </div>
    </div>

    <div class="col-flex gap-3 justify-start px-2">
      <div>
        <CollapseInfo class="group-collapse">
          {{ group.description || group.name }}
        </CollapseInfo>
      </div>
      <TabsFetch class="flex-1 min-h-screen" :tabsMap="tabsMap" />
    </div>
  </div>
</template>

<script>
import { computed } from "vue";
import ImgView from "@/components/Media/Images/ImgView.vue";
import ImgCanvas from "@/components/Media/Images/ImgCanvas.vue";
import GlassMenu from "@/components/UI/GlassMenu";
import CollapseInfo from "@/components/UI/CollapseInfo.vue";
import TabsFetch from "@/components/Fetch/TabsFetch.vue";
import InviteModal from "./GroupInvite/InviteModal.vue";
import permission from "./GroupRoles/permission.js";
import commonActions from "./commonActions.js";

export default {
  data: () => ({
    iShow: false,
    showMore: false,
    imgElm: null,
    moreMenu: null,
    tabsMap: null,
  }),

  props: {
    chat: {
      type: Object,
      required: true,
    },
  },

  computed: {
    group() {
      return this.chat;
    },

    role() {
      return this.group.user_role;
    },

    url() {
      return this.group.url;
    },

    socket() {
      return this.$session.socket;
    },
  },

  created() {
    this.setUpMenu();
    this.setUpTabs();
  },

  methods: {
    async showInvite() {
      this.iShow = true;
    },

    showSettings() {
      this.$group.showSettings = true;
    },

    setUpMenu() {
      this.moreMenu = [
        {
          label: "Invite",
          icon: "fa-solid fa-user-plus",
          cb: this.showInvite,
          hidden: computed(() => !this.canAdd),
        },
        { label: "Settings", icon: "fa-solid fa-gear", cb: this.showSettings },
        {
          label: "Leave",
          icon: "fa-solid fa-right-from-bracket",
          cls: "text-error",
          cb: this.leaveGroup,
          hidden: computed(() => this.isOwner),
        },
      ];
    },

    setUpTabs() {
      const url = this.group.url;
      const fileUrl = `${url}files`;
      this.tabsMap = {
        members: {
          manual: true,
          attrs: {
            group: this.group,
            path: "Group/GroupMembers/MembersFetch.vue",
          },
        },
        images: {
          url: `${fileUrl}?type=image`,
          path: "Media/Slides/ImagesSlide.vue",
          passAs: "files",
        },
        videos: {
          url: `${fileUrl}?type=video`,
          path: "Media/Slides/VideosSlide.vue",
          passAs: "files",
        },
        audios: {
          url: `${fileUrl}?type=audio`,
          path: "Media/List/AudiosList.vue",
          passAs: "files",
        },
      };
    },
  },

  components: {
    ImgView,
    ImgCanvas,
    GlassMenu,
    CollapseInfo,
    TabsFetch,
    InviteModal,
  },
  mixins: [permission, commonActions],
};
</script>

<style scoped>
.side-top {
  @apply relative p-3 px-3
  overflow-hidden rounded-b-3xl;
}

.side-top::before {
  @apply content-[''] absolute inset-0 bg-base-content/30 -z-20;
}

.more-box {
  @apply flex flex-col gap-1 items-end py-2 
  absolute overflow-hidden justify-start
  inset-0 right-2 z-10 pointer-events-none;
}

.more-box > * {
  @apply pointer-events-auto;
}

.more-menu {
  @apply relative origin-top-right;
}

.group-more-btn {
  @apply text-xl rounded-full bg-black/20 
  hover:bg-black/50 backdrop-blur-sm
   text-white/80
  px-4 aspect-square border-none;
}

.img-canvas {
  @apply absolute w-full h-full
  inset-0 object-center object-cover 
  blur-lg scale-110 brightness-[0.8]
  -z-10;
}

.group-img-box {
  @apply relative h-60 rounded-2xl overflow-hidden 
  backdrop-blur-0 shadow-lg;
}

.side-card-content {
  @apply flex items-center justify-between 
  p-2 px-4 bg-base-300/80 backdrop-blur-lg 
  text-base-content/80
  rounded-3xl mt-3;
}

.group-stats {
  @apply flex items-center gap-2;
}

.group-stats > * {
  @apply flex text-base items-center font-bold gap-1;
}

.invite-btn {
  @apply bg-primary/90 border-none 
  rounded-2xl text-white py-3
  px-4 text-lg;
}
</style>
