<template>
  <div class="root">
    <div class="img-box">
      <ImgView
        class="full-img"
        :showOpButtons="false"
        :file="{ url: user.photo }"
        alt=""
      />
      <div class="title-box">
        <h6 class="text-secondary text-2xl">
          {{ user.full_name }}
        </h6>
        <p class="text-white/70 flex text-base font-bold gap-0.5">
          <span class="text-primary">
            <i class="fa-solid fa-at"></i>
          </span>
          {{ user.username }}
        </p>
      </div>
    </div>
    <div class="p-3 px-4 bg-base-300 rounded-xl flex gap-2 items-start">
      <span class="text-3xl opacity-70"
        ><i class="fa-solid fa-circle-exclamation"></i
      ></span>
      <div>
        <p class="opacity-70">Bio</p>
        <div class="break-words">
          {{ user.bio || "Empty" }}
        </div>
      </div>
    </div>
    <Tabs :tabs="tabs" v-model="current" />
    <KeepAlive>
      <SideFiles
        :key="currComponent"
        :currentComponent="currComponent"
        :url="url"
      />
    </KeepAlive>
  </div>
</template>

<script>
import ImgView from "@/components/Media/ImgView.vue";
import Tabs from "@/components/UI/Tabs.vue";
import SideFiles from "./SideFiles.vue";

export default {
  data: () => ({
    tabs: [
      { label: "images", val: "image" },
      { label: "videos", val: "video" },
      { label: "audios", val: "audio" },
    ],
    current: "image",
  }),

  props: {
    user: {
      type: Object,
      required: true,
    },
    filesUrl: {
      type: String,
      required: true,
    },
  },

  computed: {
    url() {
      return `${this.filesUrl}?type=${this.current}`;
    },
    fileComponents() {
      return {
        image: "ImagesSlide",
        video: "VideosSlide",
        audio: "AudiosList",
      };
    },
    currComponent() {
      return this.fileComponents[this.current];
    },
  },

  methods: {
    tabSelected(tab) {
      this.current = this.fileComponents[tab] || this.fileComponents["image"];
    },
  },

  components: { ImgView, SideFiles, Tabs },
};
</script>

<style scoped>
.root {
  @apply p-4 overflow-y-auto
  bg-base-200 flex flex-col gap-3;
}

.img-box {
  @apply rounded-2xl flex-shrink-0 overflow-hidden h-60 relative;
}

.img-box::before {
  content: "";
  @apply absolute z-10 pointer-events-none
  inset-0 bg-gradient-to-t 
  from-[rgba(0,0,0,0.65)] via-30% 
  via-transparent to-transparent;
}

.title-box {
  @apply absolute z-10 bottom-2 left-2;
}
</style>
