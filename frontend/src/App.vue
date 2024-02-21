<template>
  <div v-if="loaded" class="app-root">
    <Flashes class="z-[10000]" />
    <Session v-if="$session.isAuthenticated" />
    <Guest v-else />
  </div>
</template>

<script>
import Flashes from "@/components/Flashes";
import Session from "@/components/Session.vue";
import Guest from "@/components/Guest.vue";

export default {
  data() {
    return {
      // defines if app is loaded
      loaded: false,
    };
  },
  props: {
    loadRouter: {
      type: Function,
      required: true,
    },
  },

  async created() {
    const promise = this.$session.loadSession();

    await this.$session.animate(promise);
    this.loadRouter();
    this.loaded = true;
  },

  components: { Flashes, Session, Guest },
};
</script>

<style scoped>
.app-root {
  @apply bg-base-300;
  background-image: url("@/assets/images/bg-pattern.svg");
}
</style>

<style>
@import "@/assets/base.css";
@import "@/assets/main.css";
@import "@/assets/animations.css";
</style>
