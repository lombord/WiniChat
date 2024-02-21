<template>
  <div class="msg-root" v-if="flashes.size">
    <div class="msg-box">
      <TransitionGroup name="flash">
        <Flash
          v-for="[id, flash] in flashes.entries()"
          :key="id"
          :flash="flash"
          :flashId="id"
          @remove="this.$flashes.removeFlash(id)"
        />
      </TransitionGroup>
    </div>
  </div>
</template>

<script>
import Flash from "./Flash.vue";
export default {
  computed: {
    flashes() {
      return this.$flashes.messages;
    },
  },
  components: { Flash },
};
</script>

<style scoped>
.msg-root {
  @apply fixed w-full top-4 pointer-events-none
   flex justify-center z-[100] px-2;
}

.msg-box {
  @apply flex flex-col gap-2 msg-root;
  max-width: 500px;
}

.flash-enter-active,
.flash-leave-active {
  @apply transition;
}

.flash-enter-from,
.flash-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}
</style>
