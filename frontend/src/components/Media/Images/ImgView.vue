<template>
  <BlurryImg @click="show = true" :url="file.url" v-bind="$attrs" />
  <ImgModalView v-if="show" v-model:show="show" :file="file" />
</template>

<script>
import ImgModalView from "@/components/Media/Modals/ImgModalView.vue";
import BlurryImg from "./BlurryImg.vue";
import fileMixin from "@/mixins/fileMixin.js";

export default {
  data: () => ({
    show: false,
  }),

  mixins: [fileMixin],
  inheritAttrs: false,
  components: { ImgModalView, BlurryImg },
};
</script>

<style scoped></style>
