<template>
  <div>
    <video
      @loadedmetadata="rewindVideo"
      class="full-img"
      :src="file.url"
      muted
      loop
      autoplay
    />
  </div>
</template>

<script>
export default {
  props:{
    file: {
      type: Object,
      required: true,
    },
  },
  methods: {
    rewindVideo({ target }) {
      target.currentTime = target.duration / 2;
    },
  },
};
</script>

<style scoped></style>
