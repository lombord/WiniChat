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
  @apply px-4 sm:px-7 md:px-10 py-5 sm:py-10 md:py-14 
   dark:bg-base-100 rounded-md mx-auto max-w-md
   border border-primary/70
   drop-shadow;
}
</style>
