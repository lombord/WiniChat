<template>
  <CenterBox class="min-h-screen login-root">
    <div ref="loginBox" class="main-box">
      <h2 class="text-primary-medium text-center mb-6 pb-2 font-bold">Login</h2>
      <Form ref="form" v-bind="$data" @validated="login" />
      <p class="text-base text-center mt-6 text-base-content/80">
        Haven't signed up yet?
        <router-link
          class="text-primary-medium font-bold"
          :to="{ name: 'register' }"
        >
          Sign Up
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
  name: "LoginView",
  data() {
    return {
      fields: {
        email: {
          attrs: {
            type: "email",
          },
        },
        password: {
          attrs: {
            type: "password",
          },
          widget: "wPassword",
        },
      },
      isSession: false,
      submitLabel: "login",
      prevent: true,
      fetchOptions: false,
    };
  },

  computed: {
    loginElm() {
      return this.$refs.form.$refs.submitBtn;
    },
  },

  mixins: [login],

  components: {
    Form,
    CenterBox,
  },
};
</script>

<style scoped>
.main-box.load-anim::after {
  @apply loading-ring;
}
</style>
