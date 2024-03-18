<template>
  <ImgInput :src="user.photo" @selected="saveImg" />
</template>

<script>
import ImgInput from "@/components/Forms/Widgets/ImgInput.vue";

export default {
  computed: {
    user() {
      return this.$session.user;
    },
  },

  methods: {
    async saveImg(img) {
      let data = new FormData();
      data.append("photo", img);
      try {
        ({ data } = await this.$session.patch("session/", data));
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

<style scoped></style>
