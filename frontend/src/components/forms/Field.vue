<template>
  <div>
    <label v-if="field.label" :for="field_id">{{ field.label }}</label>
    <TInput
      class="w-full"
      :class="{ 'error-field': !isValid && !this.field.value }"
      :name="name"
      :id="field_id"
      v-model="field.value"
      v-bind="field.attrs"
    />
    <ul class="mt-1" v-if="!isValid">
      <li class="error-msg" v-for="(err, i) in field.errors" :key="i">
        {{ err }}
      </li>
    </ul>
    <div v-if="field.help_text.length && isValid" class="help-text">
      <p v-for="(help, i) in field.help_text" :key="i">{{ help }}</p>
    </div>
  </div>
</template>

<script>
import TInput from "./TInput.vue";

export default {
  props: {
    field: {
      type: Object,
      required: true,
    },
    name: {
      type: String,
      required: true,
    },
  },
  created() {
    const attrs = this.field.attrs || (this.field.attrs = {});
    attrs.autocomplete || (this.field.autocomplete = "on");
    "required" in attrs || (attrs.required = true);
    this.field.errors = [];
    this.field.help_text || (this.field.help_text = []);
  },
  computed: {
    isValid() {
      return this.field.errors.length == 0;
    },
    field_id() {
      return `${this.name}_id`;
    },
  },
  components: {
    TInput,
  },
  inheritAttrs: false,
};
</script>

<style scoped>
.error-msg {
  @apply text-red-600;
}
.error-field {
  @apply outline-red-600 outline;
}

.help-text {
  @apply mt-2;
}

.help-text > * {
  @apply text-base;
}
</style>
