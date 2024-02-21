<template>
  <div class="group-detail-box">
    <div class="group-top">
      <div class="group-top-content">
        <div class="group-img">
          <ImgAnim
            @load="({ target }) => (imgElm = target)"
            class="full-img group-img"
            :src="group.photo"
          />
        </div>
        <div class="flex-1 truncate">
          <h5 class="text-base-content/90 capitalize">{{ group.name }}</h5>

          <div class="flex gap-2">
            <IconTag icon="fa-solid fa-users text-info">
              <span class="text-[--content-color]">{{ groupType }}</span>
            </IconTag>
            <IdTag v-if="isPublic" class="text-[--content-color]">
              {{ group.unique_name }}
            </IdTag>
          </div>

          <div class="flex gap-2">
            <IconTag icon="fa-solid fa-user-group text-primary-light">
              <span class="text-[--content-color]"
                >{{ group.members }} members</span
              >
            </IconTag>
            <IconTag icon="fa-solid fa-circle text-success">
              <span class="text-[--content-color]"
                >{{ group.online }} online</span
              >
            </IconTag>
          </div>
        </div>
      </div>
    </div>
    <ImgCanvas class="canvas-elm" v-if="imgElm" :imgElm="imgElm" />
    <div class="p-3 mt-2 z-10 relative">
      <CollapseInfo
        class="collapse-desc"
        :frozen="true"
        :defShow="true"
        title="description"
      >
        {{ group.description }}
      </CollapseInfo>
    </div>
  </div>
</template>

<script>
import ImgCanvas from "@/components/Media/Images/ImgCanvas.vue";
import CollapseInfo from "@/components/UI/CollapseInfo.vue";

export default {
  data: () => ({
    imgElm: null,
  }),

  props: {
    group: {
      type: Object,
      required: true,
    },
  },

  computed: {
    isPublic() {
      return this.group.public;
    },

    groupType() {
      return this.isPublic ? "Public" : "Private";
    },
  },

  components: { ImgCanvas, CollapseInfo },
};
</script>

<style scoped>
.group-detail-box {
  @apply relative z-10;
}

.group-top {
  @apply relative w-full z-10 p-6 px-5 pt-6 flex;
}

.group-top::before {
  @apply content-[''] absolute inset-0 -z-[1] bg-base-200/70;
}

.group-top-content {
  --content-color: theme(colors.base-content/80%);
  @apply flex items-center gap-6 flex-wrap text-[--content-color];
}

.group-detail-box .canvas-elm {
  @apply w-full h-full absolute z-[-2] 
  scale-[1.2] inset-0
  brightness-75 object-cover
  blur-md object-center;
}

.group-img {
  @apply rounded-full aspect-square h-28
  outline outline-4 outline-offset-4 
  outline-primary-medium
  overflow-hidden;
}

.collapse-desc {
  @apply bg-transparent bg-gradient-to-b from-transparent from-[-10%] to-[22%] to-base-200/90;
}
</style>
