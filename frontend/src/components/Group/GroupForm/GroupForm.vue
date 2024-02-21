<template>
  <Form
    class="p-6 py-4 bg-base-300"
    ref="form"
    :fetchOptions="false"
    :fields="fields"
    :isFormData="true"
  >
    <template v-for="(_, slot) in $slots" v-slot:[slot]="scope">
      <slot :name="slot" v-bind="scope" />
    </template>
  </Form>
</template>

<script>
import Form from "@/components/Forms";
import { ref, watch, computed } from "vue";
import wrapperMixin from "@/components/Forms/wrapperMixin.js";

export default {
  expose: ["fields", "setInitial"],

  data: () => ({
    fields: null,
  }),

  props: {
    group: {
      type: Object,
      default: null,
    },
  },

  computed: {
    canEditType() {
      const { group } = this;
      return !group || group.user_role.is_owner;
    },
  },

  created() {
    const getRef = this.group ? this.getGroupRef : this.getRef;
    const publicRef = getRef("public", false);
    this.fields = {
      photo: {
        attrs: { class: "w-28", src: getRef("photo"), required: false },
        widget: "wImage",
      },

      name: {
        attrs: {
          placeholder: "Group name",
        },
        max_length: 100,
        value: getRef("name"),
      },

      unique_name: {
        attrs: {
          placeholder: "Unique name",
          checkUrl: "groups/check-name/",
        },
        help_text: ["Group identifier name"],
        max_length: 100,
        value: getRef("unique_name"),
        widget: "wValidInput",
        hidden: computed(() => !(publicRef.value && this.canEditType)),
      },

      description: {
        max_length: 500,
        widget: "wText",
        value: getRef("description"),
      },

      public: {
        attrs: {
          label: "Public Group",
        },
        widget: "wCheck",
        value: publicRef,
        hidden: computed(() => !this.canEditType),
      },
    };
  },

  methods: {
    setInitial() {
      this.$refs.form.setInitial();
    },

    getGroupRef(name) {
      const res = ref(this.group[name]);
      watch(
        () => this.group[name],
        (val) => {
          res.value = val;
        }
      );
      return res;
    },
    getRef(name, value) {
      return ref(value);
    },
  },

  components: { Form },
  mixins: [wrapperMixin],
};
</script>

<style scoped></style>
