<template>
  <div>
    <FileInput @selected="selected" accept=".png, .jpg, .jpeg, .gif">
      <template #default="{ callback }">
        <div :class="$attrs.class" class="root" @click="callback">
          <img :src="src" class="img-view" />
          <div class="img-overlay">
            <i class="fa-solid fa-plus"></i>
          </div>
        </div>
      </template>
    </FileInput>
  </div>
</template>

<script>
import FileInput from "./FileInput.vue";

export default {
  props: {
    src: {
      type: String,
      required: true,
    },
  },
  methods: {
    selected(files) {
      this.$emit("selected", files[0]);
    },
  },
  inheritAttrs: false,
  emits: ["selected"],
  components: { FileInput },
};
</script>

<style scoped>
:deep(.root) {
  @apply relative rounded-full 
  overflow-hidden 
  aspect-square
  cursor-pointer
  w-12 md:w-16
  shadow-sm;
}

.img-view {
  @apply w-full object-cover object-center block aspect-square;
}

.img-overlay {
  @apply opacity-0 transition absolute 
  flex justify-center items-center
  transition-all duration-200
  text-white
  inset-0 bg-slate-800
  bg-opacity-10
  backdrop-blur-[1px];
}

:deep(.root:is(:hover, :focus)) > .img-overlay {
  @apply opacity-100;
}
</style>
