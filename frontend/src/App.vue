<template>
  <div v-if="loaded">
    <Flashes />
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

<style>
@import "@/assets/base.css";
@import "@/assets/animations.css";
</style>
