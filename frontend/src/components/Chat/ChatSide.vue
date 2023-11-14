<template>
  <Transition name="side">
    <div v-if="show" class="root">
      <div class="img-box">
        <img
          class="object-cover h-full w-full object-center"
          :src="user.photo"
          alt=""
        />
        <div class="title-box">
          <h6 class="text-secondary text-2xl">
            {{ user.full_name }}
          </h6>
          <p class="text-white/70 flex text-base font-bold gap-0.5">
            <span class="text-primary">
              <i class="fa-solid fa-at"></i>
            </span>
            {{ user.username }}
          </p>
        </div>
      </div>
      <div class="px-2 py-5 bg-base-300 rounded-xl">
        <div class="break-words p-1 text-center italic">
          {{ user.bio }}
        </div>
      </div>
    </div>
  </Transition>
</template>

<script>
export default {
  props: {
    user: {
      type: Object,
      required: true,
    },
    show: {
      type: Boolean,
      required: true,
    },
  },
};
</script>

<style scoped>
.root {
  @apply p-4 border-l 
  bg-base-200 flex-[0.5] flex flex-col gap-4
  border-base-content/20 
  min-w-[200px] max-w-[350px];
}

.img-box {
  @apply rounded-2xl overflow-hidden h-60
  relative;
}

.img-box::before {
  content: "";
  @apply absolute inset-0 bg-gradient-to-t 
  from-[rgba(0,0,0,0.65)] via-30% 
  via-transparent to-transparent;
}

.title-box {
  @apply absolute z-10 bottom-2 left-2;
}
</style>
