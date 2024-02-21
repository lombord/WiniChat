<template>
  <template v-if="messages.length">
    <div class="py-2 reverse-flex" :class="$attrs.class">
      <div
        v-for="[date, contexts] in messages"
        :key="date"
        class="reverse-flex"
      >
        <Contexts :contexts="contexts" v-bind="$attrs" />
        <div
          class="date-divider"
          :class="{ 'player-divider': isPlayerVisible }"
        >
          <span class="date-badge badge badge-primary">
            {{ getDivDate(date) }}
          </span>
        </div>
      </div>
    </div>
  </template>
  <div v-else class="grid place-content-center h-full">
    <h1 class="text-primary text-8xl">
      <span><i class="fa-regular fa-face-meh-blank"></i></span>
    </h1>
  </div>
</template>

<script>
import moment from "moment";
import Contexts from "./Contexts.vue";

export default {
  props: {
    messages: {
      type: Array,
      required: true,
    },
  },

  computed: {
    isPlayerVisible() {
      return !!this.$tracks.component;
    },
  },

  methods: {
    getDivDate(date) {
      return moment(date).calendar(null, {
        sameDay: "[Today]",
        nextWeek: "dddd",
        lastDay: "[Yesterday]",
        lastWeek: "dddd",
        sameElse: "DD/MM/YYYY",
      });
    },
  },

  inheritAttrs: false,
  components: { Contexts },
};
</script>

<style scoped>
.date-divider {
  @apply text-center pointer-events-none 
  sticky top-20 lg:top-24 z-10 py-2;
}

.player-divider {
  @apply top-32;
}

.date-badge {
  @apply text-base  
  bg-primary-light/60 p-3
  text-white border-none
  drop-shadow;
}
</style>
