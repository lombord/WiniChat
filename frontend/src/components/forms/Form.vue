<template>
  <form
    novalidate
    v-if="loaded"
    @submit.prevent="formSubmitted"
    autocomplete="on"
    class="flex flex-col gap-3"
  >
    <div
      class="flex flex-col gap-3"
      :class="{ 'pointer-events-none': disabled }"
    >
      <template v-for="(field, key) in fields" :key="key">
        <Field
          v-show="!field.hidden || !disabled"
          :name="key"
          :field="field"
          :disabled="disabled"
        />
      </template>
    </div>
    <slot name="submitBtn" :submitLabel="submitLabel">
      <button ref="submitBtn" type="submit" class="submit-btn click-anim">
        {{ submitLabel }}
      </button>
    </slot>
  </form>
</template>

<script>
import Field from "./Field.vue";

export default {
  // Form components that works with server
  data() {
    return {
      loaded: false,
    };
  },

  props: {
    // fields for form
    fields: {
      type: Object,
      required: true,
    },
    // Label for submit button
    submitLabel: {
      type: String,
      default: "Submit",
    },
    // axios config object
    config: {
      type: Object,
    },
    // defines whether use session request or standard
    isSession: {
      type: Boolean,
      default: true,
    },
    // Message when the form is successfully finished
    successMessage: {
      type: String,
      default: null,
    },

    // defines whether prevent send process request
    // after client side validation
    prevent: {
      type: Boolean,
      default: false,
    },
    // defines whether fetch options from server
    fetchOptions: {
      type: Boolean,
      default: true,
    },

    disabled: {
      type: Boolean,
    },
  },

  async created() {
    this.fetchOptions && (await this.fetchServerOptions());
    this.loaded = true;
  },

  computed: {
    data() {
      // body data to send to server
      const entries = Object.entries(this.fields).reduce(
        (array, [key, field]) => {
          if (field.attrs.required || field.value) {
            array.push([key, field.value]);
          }
          return array;
        },
        []
      );
      return Object.fromEntries(entries);
    },
    request() {
      // axios request object
      if (this.isSession) return this.$session.request;
      return this.$request;
    },
  },

  methods: {
    // fetches options from given config url
    async fetchServerOptions() {
      const promise = this.request({ url: this.config.url, method: "options" });
      const response = await this.$session.animate(promise);
      const method = this.config.method.toUpperCase();
      const options = response.data.actions[method];
      this.setServerOptions(options);
    },

    // sets server options after fetching
    setServerOptions(options) {
      options = this.getWriteOnly(options);
      options.forEach(([key, op]) => {
        const field = this.fields[key] || (this.fields[key] = { attrs: {} });
        const attrs = field.attrs || (field.attrs = {});
        attrs.required = op.required;
        field.max_length = op.max_length;
        attrs.placeholder || (attrs.placeholder = op.label);
      });
    },

    // gets options only for form
    getWriteOnly(options) {
      const filtered = Object.entries(options).filter(
        ({ 1: { read_only } }) => !read_only
      );
      return filtered;
    },

    // called when form is submitted
    formSubmitted() {
      if (this.isAllValid()) {
        if (!this.prevent) {
          return this.submit();
        }
        return this.$emit("validated", this.data);
      }
      this.$flashes.error("Form is invalid please try again!");
    },
    // Checks if all fields are valid
    isAllValid() {
      const isValid = Object.values(this.fields).reduce((val, field) => {
        field.errors = [];

        if (field.attrs.required && !field.value) {
          field.errors = ["This field is required!"];
          return false;
        }
        if (!field.value) return val && true;

        const { max_length } = field;
        if (max_length && field.value.length > max_length) {
          field.errors = [`Max length must be ${max_length}`];
          return false;
        }
        return val && (!field.validate || field.validate(this.fields));
      }, true);
      return isValid;
    },

    // submits form and emits succeed event on successful
    // response
    async submit() {
      const config = { ...this.config, data: this.data };
      const promise = this.request(config);
      const elm = this.$refs.submitBtn;
      try {
        const response = await this.$session.animate(promise, elm);
        const msg = this.successMessage;
        msg && this.$flashes.success(msg);
        this.$emit("succeed", response, this.data);
      } catch (error) {
        this.$flashes.error("Something went wrong!");
        this.setErrors(error.response.data);
      }
    },

    // sets errors from response
    setErrors(errorDict) {
      Object.entries(errorDict).forEach(([key, errors]) => {
        const field = this.fields[key];
        field.errors = errors;
      });
    },
  },
  components: {
    Field,
  },
};
</script>

<style scoped>
.submit-btn {
  @apply btn btn-primary mt-2 capitalize 
  no-animation
  text-xl;
}

.submit-btn.load-anim::after {
  @apply loading-spinner text-primary-content !important;
  width: 8%;
}
</style>
