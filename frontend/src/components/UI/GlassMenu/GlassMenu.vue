<template>
  <Transition name="pop">
    <KeepAlive>
      <TagComp tag="div" @mouseup.stop class="glass-box" v-if="show">
        <TransitionGroup name="fade">
          <template v-for="(option, i) in menu" :key="i">
            <div v-show="!option.hidden">
              <GlassBtn
                v-if="!option.nested"
                :option="option"
                @click.stop="selected(option, i)"
              />
              <NestedGlass :option="option" v-else>
                <KeepAlive>
                  <component
                    :is="option.path ? 'DynamicComp' : 'GlassMenu'"
                    :key="option.path || option.label"
                    v-if="option.hoverShow"
                    :path="option.path"
                    class="nested-menu glass-box"
                    v-bind="option.nested"
                    v-model:show="nestedShow"
                    :hoverShow="option.hoverShow"
                  />
                </KeepAlive>
              </NestedGlass>
            </div>
          </template>
        </TransitionGroup>
      </TagComp>
    </KeepAlive>
  </Transition>
</template>

<script>
import context from "../context.js";
import GlassBtn from "./GlassBtn.vue";
import NestedGlass from "./NestedGlass.vue";
import DynamicComp from "@/components/Utils/DynamicComp.vue";
import TagComp from "@/components/Utils/TagComp.vue";

export default {
  expose: ["$el"],
  name: "GlassMenu",

  data: () => ({
    currPromise: null,
  }),

  computed: {
    nestedShow: {
      get() {
        return this.show;
      },
      set(val) {
        this.$emit("update:show", val);
      },
    },
  },

  methods: {
    async selectedAC(option) {
      if (option.cb) {
        await option.cb(...this.extraArgs);
      }
      this.$emit("chosen");
      this.$emit("update:show", false);
    },
    selected(option) {
      if (this.currPromise) return;
      option.loading = true;
      this.currPromise = this.selectedAC(option).finally(() => {
        option.loading = false;
        this.currPromise = null;
      });
    },
  },

  mixins: [context],
  components: { GlassBtn, NestedGlass, DynamicComp, TagComp },
};
</script>

<style scoped>
:is(.glass-box, :deep(.glass-box)) {
  @apply flex flex-col p-1 relative
  z-10 w-[170px];
}

:is(.glass-box, :deep(.glass-box))::before {
  @apply content-[''] absolute border border-base-content/5 
  shadow-[0.1rem_0.1rem_0.2rem] shadow-black/5 origin-top-left
  rounded-2xl inset-0 -z-10 bg-base-100/60 backdrop-blur-lg;
}

:is(.glass-box, :deep(.glass-box)).load-anim {
  @apply min-h-[100px];
}

:is(.glass-box, :deep(.glass-box)).load-anim::after {
  @apply text-base-content/90 
  loading-ring max-h-[70px];
}
</style>
