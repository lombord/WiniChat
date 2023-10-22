<template>
  <div class="person-box">
    <div>
      <img class="round-img w-14" :src="person.photo" />
    </div>
    <div class="flex-1 truncate">
      <h5 class="text-primary">
        {{ person.full_name }}
      </h5>
      <h6 class="text-base-content/80">
        <i class="fa-solid fa-at text-secondary"></i>
        {{ person.username }}
      </h6>
    </div>
    <div>
      <button
        @click.once="({ target }) => $emit('chosen', person, target)"
        class="chat-btn"
      >
        Chat
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>
.person-box {
  @apply px-2 py-3 bg-base-200
  flex items-center gap-2
  cursor-pointer
  rounded-xl
  hover:bg-primary/20;
}

.chat-btn {
  @apply btn btn-primary;
}
.chat-btn.load-anim::after {
  @apply text-current loading-spinner;
}
</style>
