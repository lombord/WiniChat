<template>
  <div @click="selectImg" class="root">
    <input
      ref="imgInput"
      @input="changed"
      accept=".png, .jpg, .jpeg, .gif"
      class="img-input"
      type="file"
    />
    <img :src="src" class="img-view" />
    <div class="img-overlay">
      <i class="fa-solid fa-plus"></i>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    src: {
      type: String,
      required: true,
    },
  },
  methods: {
    selectImg() {
      const ev = new MouseEvent("click");
      this.$refs.imgInput.dispatchEvent(ev);
    },
    changed(e) {
      this.$emit("selected", e.target.files[0]);
    },
  },
};
</script>

<style scoped>
.root {
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

.img-input {
  @apply hidden;
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

.root:is(:hover, :focus) > .img-overlay {
  @apply opacity-100;
}
</style>
