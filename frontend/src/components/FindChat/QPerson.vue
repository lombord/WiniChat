<template>
  <div class="person-box" @click="$profile.show(person.id)">
    <div>
      <ImgAnim class="round-img w-14" :src="person.photo" />
    </div>
    <div class="flex-1 truncate">
      <h6 class="text-base-content/85">
        {{ person.full_name }}
      </h6>
      <IdTag>
        {{ person.username }}
      </IdTag>
    </div>
    <div>
      <button
        @click.capture.once.stop="
          ({ target }) => $emit('pChosen', person, target)
        "
        class="chat-btn spinner-on-load"
      >
        <i class="fa-solid fa-user-plus"></i>
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
    person() {
      return this.qItem;
    },
  },
  emits: ["pChosen"],
};
</script>

<style scoped>
.chat-btn {
  @apply btn btn-primary rounded-xl;
}
</style>
