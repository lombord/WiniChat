<template>
  <FileInput @selected="selected" accept=".png, .jpg, .jpeg, .gif">
    <template #default="{ callback }">
      <div class="img-box" :class="rootCls">
        <div class="box-wrapper">
          <div class="img-wrapper" :class="$attrs.class" @click="callback">
            <ImgAnim v-if="currSrc" :src="currSrc" class="full-img img-prev" />
            <div class="img-overlay">
              <button class="icon-btn bg-transparent">
                <i class="fa-solid fa-plus"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </template>
  </FileInput>
</template>

<script>
import FileInput from "./FileInput.vue";

export default {
  data: () => ({
    blobUrl: null,
  }),

  props: {
    src: {
      type: String,
      default: null,
    },

    modelValue: {
      default: null,
    },

    rootCls: {
      default: null,
    },
  },

  computed: {
    currSrc() {
      return this.blobUrl || this.src;
    },
  },

  beforeUnmount() {
    const { blobUrl } = this;
    if (blobUrl) {
      URL.revokeObjectURL(blobUrl);
    }
  },

  methods: {
    selected([file]) {
      if (file) {
        this.blobUrl = URL.createObjectURL(file);
        this.$emit("selected", file);
        this.$emit("update:modelValue", file);
      }
    },
  },

  watch: {
    blobUrl(nVal, oVal) {
      if (oVal && nVal != oVal) {
        URL.revokeObjectURL(oVal);
      }
    },

    src(nVal, oVal) {
      if (nVal && nVal != oVal) {
        this.blobUrl = null;
      }
    },
  },

  inheritAttrs: false,
  emits: ["selected", "update:modelValue"],
  components: { FileInput },
};
</script>

<style scoped>
.img-box {
  @apply flex justify-center;
}

.box-wrapper {
  @apply relative;
}

.box-wrapper::before {
  @apply content-[''] absolute inset-0 z-[100] pointer-events-none
  outline outline-[3px] outline-offset-[3px] outline-primary-light
  rounded-full;
}

.img-wrapper {
  @apply relative rounded-full 
  overflow-hidden   
  aspect-square bg-base-100
  cursor-pointer
  w-14 md:w-16
  shadow-sm;
}

.img-wrapper:is(:hover, :focus) > .img-overlay {
  @apply opacity-100;
}

:deep(.img-prev.load-anim::after) {
  @apply max-w-[none] h-full;
}

.img-overlay {
  @apply opacity-0 transition absolute 
  flex justify-center items-center duration-200
  text-white 
  inset-0 bg-black/20
  backdrop-blur-[1px];
}
</style>
