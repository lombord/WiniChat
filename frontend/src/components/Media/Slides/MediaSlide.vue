<template>
  <component :is="modal" :file="current">
    <slot :file="current" />
    <template #contentOut>
      <div class="arrows-box">
        <button
          @click.stop="currIdx--"
          class="modal-btn"
          :class="{ invisible: !currIdx }"
        >
          <i class="fa-solid fa-chevron-left"></i>
        </button>
        <button
          @click.stop="currIdx++"
          class="modal-btn"
          :class="{ invisible: isLast }"
        >
          <i class="fa-solid fa-chevron-right"></i>
        </button>
      </div>
    </template>
  </component>
</template>

<script>
import { defineAsyncComponent } from "vue";
import slideMixin from "./slideMixin.js";

export default {
  props: {
    modal: {
      type: String,
      default: "Modal",
    },
  },

  components: {
    Modal: defineAsyncComponent(() => import("@/components/UI/Modal.vue")),
    ImgModalView: defineAsyncComponent(() =>
      import("../Modals/ImgModalView.vue")
    ),
    VideoModalView: defineAsyncComponent(() =>
      import("../Modals/VideoModalView.vue")
    ),
  },
  mixins: [slideMixin],
};
</script>

<style scoped>
.arrows-box {
  @apply fixed pointer-events-none inset-0 z-10 
  px-5
  flex justify-between items-center;
}

.arrows-box > * {
  @apply pointer-events-auto;
}
</style>
