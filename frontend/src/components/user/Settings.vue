<template>
  <Modal class="set-box">
    <div class="photo-box">
      <div class="photo-wrap online avatar">
        <PhotoEdit class="w-28 photo" rootCls="photo-root" />
      </div>
    </div>
    <div class="p-4 mt-2 md:p-4.5 flex-1 overflow-y-auto">
      <Form :fields="fields" v-bind="$data" @succeed="updateProfile">
        <template v-if="disabled" #submitBtn>
          <button
            type="button"
            @click="disabled = false"
            class="submit-btn mt-2"
          >
            Edit
          </button>
        </template>
      </Form>
      <button
        @click="cancelChanges"
        v-if="!disabled"
        class="cancel-btn w-btn click-anim"
      >
        Cancel
      </button>
    </div>
  </Modal>
</template>

<script>
import { computed } from "vue";

import Modal from "@/components/UI/Modal.vue";
import Form from "@/components/Forms/Form.vue";

import PhotoEdit from "./PhotoEdit.vue";

export default {
  data() {
    const forceShow = computed(() => this.disabled);
    return {
      fields: {
        username: {
          attrs: { placeholder: "Username" },
          max_length: 40,
        },
        first_name: {
          attrs: { placeholder: "First Name" },
          max_length: 50,
        },
        last_name: {
          attrs: { placeholder: "Last Name" },
          max_length: 50,
        },
        bio: {
          max_length: 500,
          widget: "wText",
          attrs: { required: false },
        },
        old_password: {
          max_length: 60,
          widget: "wPassword",
          hidden: forceShow,
          attrs: { required: false, placeholder: "Old Password" },
        },
        password: {
          max_length: 60,
          widget: "wPassword",
          hidden: forceShow,
          attrs: { required: false },
        },
      },
      submitLabel: "save",
      config: {
        url: "session/",
        method: "patch",
      },
      successMessage: "Profile has been updated.",
      fetchOptions: false,
      disabled: true,
    };
  },

  computed: {
    user() {
      return this.$session.user;
    },
  },

  created() {
    this.setInitial();
  },

  methods: {
    setValue(field, value) {
      this.fields[field].value = value;
    },
    updateProfile({ data }) {
      Object.assign(this.user, data);
      this.cancelChanges();
    },

    setInitial() {
      const { fields } = this;
      for (const key of Object.keys(fields)) fields[key].value = "";

      this.setValue("username", this.user.username);
      this.setValue("first_name", this.user.first_name);
      this.setValue("last_name", this.user.last_name);
      this.setValue("bio", this.user.bio || "");
    },

    cancelChanges() {
      this.disabled = true;
      this.setInitial();
    },
  },

  components: { Modal, Form, PhotoEdit },
};
</script>

<style scoped>
:deep(.set-box) {
  @apply overflow-hidden flex flex-col max-w-[550px] p-0;
}

:deep(.photo-root .box-wrapper::before) {
  @apply content-none;
}

.photo-box {
  @apply py-3.5 bg-primary 
  flex justify-center;
}

.photo-wrap {
  @apply relative;
}

:deep(.photo::before) {
  content: "";
  @apply absolute inset-0 border-2 
  rounded-full z-[1];
}

.cancel-btn {
  @apply w-full btn-secondary mt-2;
}
</style>
