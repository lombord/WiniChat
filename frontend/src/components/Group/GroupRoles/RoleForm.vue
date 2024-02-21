<template>
  <Form ref="form" :fields="fields" :fetchOptions="false">
    <template v-for="(_, slot) in $slots" v-slot:[slot]="scope">
      <slot :name="slot" v-bind="scope" />
    </template>
  </Form>
</template>

<script>
import Form from "@/components/Forms/Form.vue";
import wrapperMixin from "@/components/Forms/wrapperMixin.js";
import { ref, watch, computed } from "vue";

export default {
  expose: ["fields", "setInitial"],

  data: () => ({
    fields: null,
  }),

  props: {
    group: {
      type: Object,
      required: true,
    },
    editRole: {
      type: Object,
      default: null,
    },
  },

  computed: {
    role() {
      return this.group.user_role;
    },
  },

  created() {
    const { getPerm } = this;
    const superRef = getPerm("super_admin", false, true);

    this.fields = {
      name: {
        attrs: { placeholder: "Role Name" },
        max_length: 30,
        value: getPerm("name"),
      },

      send_msg: {
        attrs: { fakeCheck: superRef, label: "Send messages" },
        widget: "wCheck",
        value: getPerm("send_msg", true),
      },

      delete_msg: {
        attrs: { fakeCheck: superRef, label: "Delete messages" },
        widget: "wCheck",
        value: getPerm("delete_msg", false),
      },
      add_user: {
        attrs: { fakeCheck: superRef, label: "Add members" },
        widget: "wCheck",
        value: getPerm("add_user", true),
      },
      kick_user: {
        attrs: { fakeCheck: superRef, label: "Kick members" },
        widget: "wCheck",
        value: getPerm("kick_user", false),
      },
      ban_user: {
        attrs: { fakeCheck: superRef, label: "Ban members" },
        widget: "wCheck",
        value: getPerm("ban_user", false),
      },
      unban_user: {
        attrs: { fakeCheck: superRef, label: "Unban members" },
        widget: "wCheck",
        value: getPerm("unban_user", false),
      },
      edit_group: {
        attrs: { fakeCheck: superRef, label: "Edit group" },
        widget: "wCheck",
        value: getPerm("edit_group", false),
      },
      manage_role: {
        attrs: {
          fakeCheck: superRef,
          label: "Manage roles",
        },
        widget: "wCheck",
        value: getPerm("manage_role", false),
      },
      super_admin: {
        attrs: {
          label: "Super Admin",
        },
        widget: "wCheck",
        value: superRef,
      },
      priority: {
        attrs: {
          placeholder: "Priority",
          max: 100,
          class: "min-h-[55px]",
          min: computed(() => {
            try {
              return Math.min(this.role.priority + 1, 100);
            } catch (error) {
              return 100;
            }
          }),
        },
        widget: "wNumber",
        value: getPerm("priority"),
      },
    };
  },

  methods: {
    getPerm(perm, def, isRef = false) {
      if (!this.editRole) {
        return isRef ? ref(def) : def;
      }
      const res = ref(this.editRole[perm]);
      watch(
        () => this.editRole[perm],
        (val) => {
          res.value = val;
        }
      );
      return res;
    },
  },

  components: { Form },
  mixins: [wrapperMixin],
};
</script>

<style scoped></style>
