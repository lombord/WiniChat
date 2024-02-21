<template>
  <div :id="`field_${name}`">
    <div class="col-flex gap-1">
      <label class="field-label" v-if="field.label" :for="field_id">{{
        field.label
      }}</label>
      <DynamicComp
        :path="widgetPath"
        :class="{ 'error-field': !isValid && !this.field.value }"
        :name="name"
        :id="field_id"
        v-model="field.value"
        :maxLength="field.max_length"
        v-bind="Object.assign(field.attrs, $attrs)"
      >
        <template #fallback>
          <div
            v-if="['wInput', 'wPassword'].includes(widgetName)"
            class="py-6 load-sk rounded-xl"
          ></div>
          <div
            v-else-if="widgetName == 'wText'"
            class="py-10 load-sk rounded-xl"
          ></div>
          <div
            v-else-if="widgetName == 'wCheck'"
            class="p-3 load-sk flex items-center justify-between rounded-xl"
          >
            <div class="p-2 rounded-full shrink w-[100px] max load-sk"></div>
            <div class="p-3.5 px-6 load-sk rounded-full"></div>
          </div>
          <div
            v-else-if="widgetName == 'wNumber'"
            class="py-0 load-sk grid grid-cols-3 overflow-hidden rounded-xl"
          >
            <div class="p-9 load-sk"></div>
            <div class="load-sk col-start-3"></div>
          </div>
        </template>
      </DynamicComp>
    </div>
    <ul class="error-msgs col-flex gap-1" v-if="!isValid">
      <li class="error-msg" v-for="(err, i) in field.errors" :key="i">
        {{ err }}
      </li>
    </ul>
    <div v-else-if="field.help_text.length" class="col-flex gap-1 help-msgs">
      <p class="help-msg" v-for="(help, i) in field.help_text" :key="i">
        {{ help }}
      </p>
    </div>
  </div>
</template>

<script>
import DynamicComp from "@/components/Utils/DynamicComp.vue";

const _wPrefix = "Forms/Widgets/";

const widgetPaths = {
  wInput: `${_wPrefix}PHInput.vue`,
  wValidInput: `${_wPrefix}ValidInput.vue`,
  wText: `${_wPrefix}TextBox.vue`,
  wPassword: `${_wPrefix}PasswordInput.vue`,
  wCheck: `${_wPrefix}CheckWidget.vue`,
  wNumber: `${_wPrefix}NumberInput.vue`,
  wFile: `${_wPrefix}FileInput.vue`,
  wImage: `${_wPrefix}ImgInput.vue`,
};

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

  widgetPaths,

  computed: {
    isValid() {
      return this.field.errors.length == 0;
    },

    field_id() {
      return `${this.name}_id`;
    },

    widgetName() {
      return this.field.widget || "wInput";
    },

    widgetPath() {
      return this.$options.widgetPaths[this.widgetName];
    },
  },

  created() {
    const attrs = this.field.attrs || (this.field.attrs = {});
    attrs.autocomplete || (this.field.autocomplete = "on");
    "required" in attrs || (attrs.required = true);
    this.field.errors = [];
    this.field.help_text || (this.field.help_text = []);
    if (this.field.showLabel && !this.field.label) {
      this.field.label = attrs.placeholder;
    }
  },

  components: { DynamicComp },
  inheritAttrs: false,
};
</script>

<style scoped>
.error-field {
  @apply outline-error outline;
}

.error-msgs,
.help-msgs {
  @apply ml-2 pt-1.5 pb-3;
}

.error-msg {
  @apply text-error/95;
}

.error-msg,
.help-msg {
  @apply text-sm leading-4 flex gap-1.5 items-center;
}

:is(.help-msg, .error-msg)::before {
  @apply content-[''] inline-block
  w-2 aspect-square opacity-80
  rounded-full bg-current;
}

.help-msg {
  @apply text-base-content/80;
}
</style>
