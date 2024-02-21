<template>
  <div class="img-box group">
    <ImgAnim class="full-img bl-img" @imgLoad="$attrs.onImgLoad" :src="url" />
    <div class="button-box">
      <button class="btn">
        <i class="fa-solid fa-eye"></i>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    url: {
      type: String,
      required: true,
    },
  },
};
</script>

<style scoped>
.img-box {
  @apply relative cursor-pointer bg-base-100 
  backdrop-blur-0;
  transform: translateZ(0);
  backface-visibility: hidden;
}

.button-box {
  @apply flex opacity-0 transition
  absolute inset-0 bg-black/20 backdrop-blur-sm  
  justify-center gap-2 p-2 px-4
  group-hover:opacity-100 flex-col;
}

.button-box > * {
  @apply bg-transparent text-2xl p-0
  text-white opacity-70 border-none;
}
</style>
