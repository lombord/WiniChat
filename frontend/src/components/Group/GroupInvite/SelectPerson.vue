<template>
  <div class="person-box" :class="{ selected: isSelected }">
    <div>
      <ImgAnim class="p-avatar round-img" :src="person.photo" />
    </div>
    <div class="flex-1 truncate text-inherit">
      <h6 class="p-name">
        {{ person.full_name }}
      </h6>
      <IdTag>
        {{ person.username }}
      </IdTag>
    </div>
    <div class="check-btn">
      <i class="fa-solid fa-circle-check"></i>
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
    isSelected: {
      type: Boolean,
      required: true,
    },
  },
};
</script>

<style scoped>
.person-box {
  @apply p-2 bg-base-200 transition
  flex items-center gap-2 cursor-pointer
  rounded-2xl hover:bg-base-content/15;
}

.selected.person-box {
  @apply bg-primary-light text-white/80;
}

.selected.person-box :is(*, :deep(*)) {
  @apply text-white/80 !important;
}

:deep(.p-avatar) {
  transition-property: outline;
  @apply w-[54px] ease-in-out duration-150 outline outline-offset-2
  outline-white/70 outline-0;
}

.selected :deep(.p-avatar) {
  @apply outline-[3px];
}

.p-name {
  @apply text-base-content/95;
}

.selected .p-name {
  @apply text-white/95;
}

.check-btn {
  @apply text-xl text-white scale-0 transition p-2;
}

.selected .check-btn {
  @apply scale-100;
}
</style>
