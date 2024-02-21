<template>
  <component
    :is="tag"
    @play="pr.paused = false"
    @pause="pr.paused = true"
    @timeupdate="pr.timeChanged"
    @durationchange="pr.durationChanged"
    @volumechange="pr.volumeChanged"
    @progress="pr.calcProgress"
    @seeking="pr.loading = true"
    @waiting="pr.loading = true"
    @loadeddata="pr.loading = false"
    @playing="pr.loading = false"
    @seeked="pr.loading = false"
    :src="pr.url"
  >
    <slot />
  </component>
</template>

<script>
export default {
  expose: ["$el"],
  props: {
    tag: {
      type: String,
      default: "audio",
    },
  },
  computed: {
    pr() {
      return this.$parent;
    },
  },
};
</script>

<style scoped></style>
