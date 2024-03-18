<template>
  <CenterBox class="min-h-screen root-box">
    <div ref="loginBox" class="main-box">
      <h2 class="text-primary-medium text-center mb-5 pb-2">Register</h2>
      <Form
        class="form-box"
        v-bind="$data"
        submitLabel="Sign Up"
        @succeed="userCreated"
      />
      <p class="text-base text-center mt-6 text-base-content/80">
        Already have an account?
        <router-link
          class="text-primary-medium font-bold"
          :to="{ name: 'login' }"
        >
          Login
        </router-link>
      </p>
    </div>
  </CenterBox>
</template>

<script>
import Form from "@/components/Forms/Form.vue";
import CenterBox from "@/components/UI/CenterBox.vue";
import login from "@/mixins/login.js";

export default {
  name: "RegisterView",

  data: () => ({
    fields: {
      username: {
        help_text: ["Your identifier name"],
        attrs: { checkUrl: "check-username/" },
        widget: "wValidInput",
      },

      email: {
        attrs: {
          type: "email",
          checkUrl: "check-user-email/",
        },
        widget: "wValidInput",
      },

      password: {
        attrs: { type: "password", autocomplete: "new-password" },
        widget: "wPassword",
        validate(field, fields) {
          if (this.value.length < 8) {
            this.errors = ["Password must be at least 8 characters!"];
          } else {
            return true;
          }
        },
      },
      password2: {
        attrs: {
          type: "password",
        },
        widget: "wPassword",
        validate(field, fields) {
          if (this.value !== fields.password.value) {
            this.errors = ["Passwords do not match!"];
          } else {
            return true;
          }
        },
      },
    },
    config: {
      url: "register/",
      method: "post",
    },
    isSession: false,
    successMessage: "Successfully Signed Up!",
  }),
  mixins: [login],
  components: {
    Form,
    CenterBox,
  },
  methods: {
    userCreated() {
      const email = this.fields.email.value;
      const password = this.fields.password.value;
      const data = { email, password };
      this.login(data);
    },
  },
};
</script>

<style scoped>
.form-box.form-loading {
  @apply min-h-[320px];
}

.form-box.load-anim::after {
  @apply loading-dots;
}
</style>
