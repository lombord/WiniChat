<template>
  <GlassMenu
    ref="context"
    class="glass-menu"
    v-model:show="showCtx"
    :style="{ top: `${oY}px`, left: `${oX}px` }"
  />
</template>

<script>
import GlassMenu from "@/components/UI/GlassMenu";

export default {
  expose: ["showContext"],

  data: () => ({
    oY: 0,
    oX: 0,
    currElm: null,
  }),

  props: {
    show: {
      type: Boolean,
      required: true,
    },
    activeCls: {
      type: String,
      default: "active-context",
    },
  },

  computed: {
    showCtx: {
      get() {
        return this.show;
      },
      set(val) {
        this.$emit("update:show", val);
      },
    },
  },

  methods: {
    async showContext({ clientX, clientY, currentTarget }) {
      this.currElm = currentTarget;
      this.showCtx = true;
      await this.$nextTick();
      const ctxElm = this.$refs.context.$el;
      const [ctxWidth, ctxHeight] = [ctxElm.clientWidth, ctxElm.clientHeight];
      const boxRect = currentTarget.getBoundingClientRect();
      const bodyRect = document.body.getBoundingClientRect();
      clientX = this.minmax(clientX, {
        min: boxRect.left,
        max: boxRect.right - ctxWidth,
      });
      clientY = this.minmax(clientY, {
        max: bodyRect.bottom - ctxHeight - 10,
      });
      [this.oX, this.oY] = [clientX, clientY];
      return ctxElm;
    },

    minmax(val, options) {
      const { min = 0, max } = options;
      return Math.max(min, Math.min(val, max));
    },
  },

  watch: {
    showCtx(val) {
      if (val) {
        this.currElm.classList.add(this.activeCls);
      } else {
        this.currElm.classList.remove(this.activeCls);
        this.currElm = null;
      }
    },
  },

  components: { GlassMenu },
};
</script>

<style scoped>
.manager-box {
  @apply relative;
}

.glass-menu {
  @apply fixed z-[100];
}
</style>
