<template>
  <Modal class="set-box" v-bind="$attrs">
    <div class="photo-box">
      <div class="photo-wrap online avatar">
        <PhotoEdit class="w-28 photo" />
      </div>
    </div>
    <div class="p-4 md:p-4.5">
      <Form
        class="gap-[6px]"
        :fields="fields"
        v-bind="$data"
        @succeed="updateProfile"
      >
        <template v-if="disabled" #submitBtn>
          <button type="button" @click="disabled = false" class="edit-btn btn">
            Edit
          </button>
        </template>
      </Form>
      <button @click="cancelChanges" v-if="!disabled" class="btn cxl-btn">
        Cancel
      </button>
    </div>
  </Modal>
</template>

<script>
import Modal from "@/components/UI/Modal.vue";
import Form from "@/components/forms/Form.vue";

import PhotoEdit from "./PhotoEdit.vue";

export default {
  data: () => ({
    fields: {
      first_name: {
        attrs: { placeholder: "First Name" },
        showLabel: true,
      },
      last_name: {
        attrs: { placeholder: "Last Name" },
        showLabel: true,
      },
      bio: {
        max_length: 255,
        label: "BIO",
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
  }),

  computed: {
    user: {
      get() {
        return this.$session.user;
      },
      set(value) {
        this.$session.user = value;
      },
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
      this.user = data;
      this.cancelChanges();
    },

    setInitial() {
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
.photo-box {
  @apply py-3.5 bg-primary 
  flex justify-center;
}

.photo-wrap {
  @apply relative;
}

.photo::before {
  content: "";
  @apply absolute inset-0 border-2 
  rounded-full z-[1];
}

.edit-btn,
.cxl-btn {
  @apply text-lg
  py-2.5 normal-case;
}

.edit-btn {
  @apply btn-primary mt-4;
}

.cxl-btn {
  @apply btn-secondary w-full mt-2;
}
</style>

<style>
.set-box {
  @apply max-w-[550px] p-0 !important;
}
</style>
