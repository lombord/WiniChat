<template>
  <div class="h-screen grid place-content-center">
    <Form
      :fields="fields"
      @validated="(d) => console.log(...d.values())"
      :isFormData="true"
      :prevent="true"
      :fetchOptions="false"
    />
  </div>
</template>

<script>
import ImgInput from "@/components/Forms/Widgets/ImgInput.vue";
import Form from "@/components/Forms";

export default {
  data: () => ({
    fields: {
      image: {
        attrs: { class: "w-28" },
        widget: "wImage",
      },
      name: {
        attrs: { placeholder: "Role Name" },
        max_length: 30,
      },
    },
  }),

  methods: {
    imgSelected(data) {
      console.log(data);
    },
  },

  components: { ImgInput, Form },
};
</script>

<style scoped></style>
