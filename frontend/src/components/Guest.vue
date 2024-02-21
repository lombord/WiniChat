<template>
  <div>
    <RouterView v-slot="{ Component }">
      <KeepAlive include="RegisterView,LoginView">
        <component :is="Component" />
      </KeepAlive>
    </RouterView>
  </div>
</template>

<script>
export default {};
</script>

<style scoped></style>
