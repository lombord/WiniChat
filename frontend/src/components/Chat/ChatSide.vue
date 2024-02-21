<template>
  <div class="root p-3 px-2 col-flex justify-start gap-3">
    <ImgOverlay :url="user.photo">
      <h6 class="text-secondary text-2xl">
        {{ user.full_name }}
      </h6>

      <IdTag class="text-white/70">
        {{ user.username }}
      </IdTag>
    </ImgOverlay>
    <CollapseInfo title="Bio">
      {{ user.bio || "Empty" }}
    </CollapseInfo>
    <TabsFetch class="flex-1 min-h-full" :tabsMap="tabsMap" />
  </div>
</template>

<script>
import ImgOverlay from "@/components/Media/Images/ImgOverlay.vue";
import CollapseInfo from "@/components/UI/CollapseInfo.vue";
import TabsFetch from "@/components/Fetch/TabsFetch.vue";

export default {
  props: {
    chat: {
      type: Object,
      required: true,
    },
  },

  computed: {
    filesUrl() {
      return this.chat.files_url;
    },
    user() {
      return this.chat.companion;
    },
    tabsMap() {
      const url = this.filesUrl;
      return {
        images: {
          url: `${url}?type=image`,
          path: "Media/Slides/ImagesSlide.vue",
          passAs: "files",
        },
        videos: {
          url: `${url}?type=video`,
          path: "Media/Slides/VideosSlide.vue",
          passAs: "files",
        },
        audios: {
          url: `${url}?type=audio`,
          path: "Media/List/AudiosList.vue",
          passAs: "files",
        },
      };
    },
  },

  components: { ImgOverlay, CollapseInfo, TabsFetch },
};
</script>

<style scoped></style>
