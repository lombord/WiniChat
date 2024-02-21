<template>
  <div class="collapse-base" :class="{ 'collapse-active': !show }">
    <slot />
    <div v-if="!frozen" @click="toggleState" class="btn-box">
      <button class="icon-btn" :class="{ 'show-btn': !show }">
        <i class="fa-solid fa-chevron-up"></i>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  data: () => ({
    show: false,
  }),

  props: {
    defShow: false,
    frozen: false,
  },

  created() {
    this.show = this.defShow;
  },

  methods: {
    toggleState() {
      if (!this.frozen) {
        this.show = !this.show;
      }
    },
  },
};
</script>

<style scoped>
.collapse-base {
  --height: 100vh;
  @apply p-3 px-4 bg-base-300/80 rounded-xl
  overflow-hidden max-h-[--height] relative;
  transition-property: max-height;
  transition-duration: 300ms;
  transition-timing-function: ease-out;
}

.collapse-active {
  --height: 100px;
}

.btn-box {
  @apply absolute bottom-0 inset-x-0 grid 
  opacity-60 hover:opacity-100 py-1
  place-content-center cursor-pointer;
}

.icon-btn {
  @apply py-1 px-1 transition;
}

.show-btn {
  @apply rotate-180;
}

.collapse-active::before {
  @apply content-[''] inset-0 absolute
  bg-gradient-to-t from-base-300 from-5% to-transparent;
}
</style>
