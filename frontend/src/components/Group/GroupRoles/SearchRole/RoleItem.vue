<template>
  <GlassBtn
    @click="$emit('chosen', role, option)"
    :class="{ 'curr-role': isCurrent }"
    :option="option"
  />
</template>

<script>
import GlassBtn from "@/components/UI/GlassMenu/GlassBtn.vue";
import trackRole from "../trackRole.js";
import { computed } from "vue";

export default {
  data: () => ({
    option: {
      label: null,
      icon: "fa-solid fa-shield-halved text-accent",
    },
  }),

  props: {
    role: {
      type: Object,
      required: true,
    },
    isCurrent: {
      type: Boolean,
      default: false,
    },
  },

  computed: {
    groupId() {
      return this.role.group;
    },
  },

  created() {
    this.option.label = computed(() => this.role.name);
  },

  components: { GlassBtn },
  mixins: [trackRole],
  emits: ["chosen"],
};
</script>

<style scoped>
.curr-role {
  @apply bg-primary-medium/90 hover:bg-primary;
}

.curr-role :deep(*) {
  @apply text-white/90 !important;
}
</style>
