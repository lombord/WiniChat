<template>
  <div class="people-box col-flex">
    <QPerson
      v-bind="$attrs"
      v-for="person in people"
      :key="person.id"
      :person="person"
    />
    <slot name="bottom"></slot>
  </div>
</template>

<script>
import QPerson from "./QPerson.vue";

export default {
  props: {
    people: {
      type: Array,
      required: true,
    },
  },
  inheritAttrs: false,
  components: { QPerson },
};
</script>

<style scoped></style>
