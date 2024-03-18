<template>
  <form
    novalidate
    :class="{ 'pointer-events-none': disabled }"
    @submit.prevent="formSubmitted"
    autocomplete="on"
    class="col-flex form-box"
  >
    <TransitionGroup name="small-pop">
      <template v-if="loaded" v-for="(field, key) in fields" :key="key">
        <Field
          v-if="!field.hidden"
          :isSession="isSession"
          :name="key"
          :field="field"
          :disabled="disabled"
        />
      </template>
    </TransitionGroup>

    <div class="pointer-events-auto">
      <slot name="submitBtn" :submitLabel="submitLabel">
        <button
          ref="submitBtn"
          type="submit"
          class="submit-btn click-anim spinner-on-load"
        >
          {{ submitLabel }}
        </button>
      </slot>
    </div>
  </form>
</template>

<script>
import Field from "./Field.vue";
import safeRequest from "@/mixins/safeRequest";

export default {
  expose: ["$refs", "setInitial"],
  // Form components that works with server
  data() {
    return {
      loaded: false,
    };
  },

  props: {
    isEditForm: {
      type: Boolean,
      default: false,
    },

    disabled: {
      type: Boolean,
      default: false,
    },

    // defines whether fetch options from server
    fetchOptions: {
      type: Boolean,
      default: true,
    },

    optionAction: {
      type: String,
      default: "POST",
    },

    // fields for form
    fields: {
      type: Object,
      required: true,
    },

    // defines whether prevent processing request
    // after client side validation
    prevent: {
      type: Boolean,
      default: false,
    },

    // Label for submit button
    submitLabel: {
      type: String,
      default: "Submit",
    },

    baseValidator: {
      type: Function,
      default: null,
    },

    // axios config object
    config: {
      type: Object,
    },

    isFormData: {
      type: Boolean,
      default: false,
    },

    cleanF: {
      type: Function,
      default: null,
    },

    getPromElm: {
      type: Function,
      default: null,
    },

    // Message when the form is successfully finished
    successMessage: {
      type: String,
      default: null,
    },
  },

  computed: {
    data() {
      return this.isFormData ? this.getFormData() : this.getJSData();
    },

    addCheck() {
      return this.isEditForm ? this.editAddCheck : this.baseAddCheck;
    },
  },

  async created() {
    if (this.fetchOptions) {
      await this.fetchServerOptions();
    }
    const { fields } = this;
    for (const key of Object.keys(fields)) {
      const field = fields[key];
      field.initial = field.value;
    }
    this.loaded = true;
  },

  methods: {
    setInitial() {
      const { fields } = this;
      for (const key in fields) {
        const field = fields[key];
        field.value = field.initial;
      }
    },

    // fetches options from given config url
    async fetchServerOptions() {
      try {
        const promise = this.request({
          url: this.config.url,
          method: "OPTIONS",
        });
        const response = await this.$session.animate(promise, this.$el);
        const options = response.data.actions[this.optionAction.toUpperCase()];
        this.setServerOptions(options);
      } catch (error) {
        return;
      }
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
        const errors = (field.errors = []);
        const { value } = field;

        if (field.attrs.required && !(value || value === false)) {
          errors.push("This field is required!");
          return false;
        }

        if (!value) return val && true;

        const { max_length } = field;
        if (max_length && value.length > max_length) {
          errors.push(`Max length must be ${max_length}`);
          return false;
        }

        return val && (!field.validate || field.validate(field, this.fields));
      }, true);
      return isValid && (!this.baseValidator || this.baseValidator());
    },

    acquirePromElm() {
      if (this.getPromElm) {
        return this.getPromElm();
      }
      return this.$refs.submitBtn || this.$el || this.$parent.$el;
    },

    baseAddCheck(field, value) {
      return field.attrs.required || value;
    },

    editAddCheck(field, value) {
      return field.initial != value && this.baseAddCheck(field, value);
    },

    getFormData() {
      const data = new FormData();
      const { addCheck } = this;
      for (const [key, field] of Object.entries(this.fields)) {
        const { value } = field;
        if (addCheck(field, value)) data.set(key, value);
      }
      return data;
    },

    getJSData() {
      const data = {};
      const { addCheck } = this;
      for (const [key, field] of Object.entries(this.fields)) {
        const { value } = field;
        if (addCheck(field, value)) data[key] = value;
      }
      return data;
    },

    // submits form and emits succeed event on successful
    // response
    async submit() {
      let { data } = this;
      if (this.cleanF) {
        data = this.cleanF(data);
      }
      const config = { ...this.config, data };
      const promise = this.request(config);
      const elm = this.acquirePromElm();
      try {
        const response = await this.$session.animate(promise, elm);
        const msg = this.successMessage;
        msg && this.$flashes.success(msg);
        this.$emit("succeed", response, data);
      } catch (error) {
        this.$flashes.error("Something went wrong!");
        this.setErrors(error?.response?.data);
        this.$emit("error", error);
      }
    },

    // sets errors from response
    setErrors(errorDict) {
      if (!(errorDict && typeof errorDict == "object")) return;
      Object.entries(errorDict).forEach(([key, errors]) => {
        const field = this.fields[key];
        if (!field) {
          this.$flashes.error(errors);
          return;
        }
        const fErrors = (field.errors = []);
        if (typeof errors != "string") {
          fErrors.push(...errors);
        } else {
          fErrors.push(errors);
        }
      });
    },
  },

  components: {
    Field,
  },
  emits: ["validated", "succeed", "error"],
  mixins: [safeRequest],
};
</script>

<style scoped>
@import "@/assets/main.css";

.form-box {
  @apply gap-3;
}

.form-box.loading-anim {
  @apply min-h-[200px];
}

:slotted(.submit-btn) {
  @apply w-btn;
}

:slotted(.submit-btn) {
  @apply no-animation btn-primary w-full;
}
</style>
