<template>
  <div ref="fetchElm" class="files-content">
    <template v-if="files.length">
      <component :is="currentComponent" :files="files" />
      <div v-int="loadNext">
        <div class="load-anim observer"></div>
      </div>
    </template>
    <h3 v-else class="text-5xl text-primary text-center">
      <i class="bi bi-folder-x"></i>
    </h3>
  </div>
</template>

<script>
import { defineAsyncComponent } from "vue";

import filesMixin from "./filesMixin.js";

export default {
  props: {
    currentComponent: {
      type: String,
      required: true,
    },
  },
  components: {
    ImagesSlide: defineAsyncComponent(() =>
      import("@/components/Media/Slides/ImagesSlide.vue")
    ),
    VideosSlide: defineAsyncComponent(() =>
      import("@/components/Media/Slides/VideosSlide.vue")
    ),
    AudiosList: defineAsyncComponent(() =>
      import("@/components/Media/List/AudiosList.vue")
    ),
  },
  mixins: [filesMixin],
};
</script>

<style scoped>
.files-content {
  @apply flex-1 min-h-[300px] overflow-x-hidden overflow-y-auto 
  rounded-xl mt-2;
}

.files-content.load-anim::after {
  @apply loading-ring;
}

.files-content::-webkit-scrollbar {
  @apply hidden;
}

.observer.load-anim {
  @apply pt-10 mt-6 after:loading-spinner after:w-10;
}

:deep(.dynamic-grid) {
  --min-size: 150px;
  @apply gap-1.5;
}

:deep(.dynamic-grid > *) {
  @apply min-h-[250px] max-h-[300px];
}
</style>
