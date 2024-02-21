<template>
  <div class="center-content">
    <div class="container">
      <div class="center-box-slot">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  @apply p-3;
}

.center-box-slot {
  @apply px-8 sm:px-10 md:px-14 
  py-14 sm:py-16 md:py-20 
  bg-base-100/60 backdrop-blur
  rounded-xl mx-auto max-w-lg
  border border-primary-medium/80;
}
</style>
