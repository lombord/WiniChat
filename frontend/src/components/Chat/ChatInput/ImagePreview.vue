<template>
  <div>
    <img class="full-img" :src="file.url" alt="" />
  </div>
</template>

<script>
export default {
  props: {
    file: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped></style>
