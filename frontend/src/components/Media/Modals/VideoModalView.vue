<template>
  <Modal class="video-modal">
    <VideoView :key="file" :file="file" />
    <template #contentOut>
      <slot name="contentOut"></slot>
    </template>
  </Modal>
</template>

<script>
import Modal from "@/components/UI/Modal.vue";

import VideoView from "../VideoView.vue";

export default {
  props: {
    file: {
      type: Object,
      required: true,
    },
  },
  components: { Modal, VideoView },
};
</script>

<style scoped>
:deep(.video-modal) {
  --min-w: 900px;
  @apply max-w-3xl p-0 rounded-2xl ;
}
</style>
