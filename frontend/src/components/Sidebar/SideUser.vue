<template>
  <div class="main-div">
    <div>
      <ImgInput :src="user.photo" @selected="saveImg" class="md:w-20" />
    </div>
    <div class="flex-1 truncate">
      <h5 class="text-primary">{{ name }}</h5>
      <p class="text-base-content/80">@{{ user.bio || user.username }}</p>
    </div>
    <div>
      <button class="logout-btn btn" @click="$router.push({ name: 'logout' })">
        <i class="fa-solid fa-right-from-bracket"></i>
      </button>
    </div>
  </div>
</template>

<script>
import ImgInput from "@/components/forms/ImgInput.vue";
export default {
  computed: {
    user() {
      return this.$session.user;
    },

    name() {
      return this.user.full_name || this.user.username;
    },
  },

  methods: {
    async saveImg(img) {
      let data = new FormData();
      data.append("photo", img);
      try {
        ({ data } = await this.$session.patch("session/", data, true));
        this.user.photo = data.photo;
        this.$flashes.info("Photo has been updated");
      } catch (err) {
        this.$flashes.error("Invalid photo please try again!");
      }
    },
  },

  components: { ImgInput },
};
</script>

<style scoped>
.main-div {
  @apply flex items-center gap-2 md:gap-3;
}

.logout-btn {
  @apply opacity-30 hover:opacity-100 
  hover:btn-primary text-xl py-2;
}
</style>
