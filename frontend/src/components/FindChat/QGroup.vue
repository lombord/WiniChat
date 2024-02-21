<template>
  <div class="group-box">
    <div>
      <ImgAnim class="round-img w-14" :src="group.photo" />
    </div>
    <div class="flex-1 truncate">
      <h6 class="text-primary-light flex items-center gap-1">
        <span class="text-secondary text-base"
          ><i class="fa-solid fa-users"></i
        ></span>
        <span>
          {{ group.name }}
        </span>
      </h6>
      <IdTag>
        {{ group.unique_name }}
      </IdTag>
    </div>
    <div>
      <button
        class="chat-btn text-base spinner-on-load"
        @click.capture.once.stop="
          ({ target }) => $emit('gChosen', group.url, target)
        "
      >
        <i class="fa-solid fa-circle-nodes"></i>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    qItem: {
      type: Object,
      required: true,
    },
  },

  computed: {
    group() {
      return this.qItem;
    },
  },

  emits: ["gChosen"],
};
</script>

<style scoped>
.group-box {
}

.chat-btn {
  @apply btn btn-primary rounded-xl;
}
</style>
