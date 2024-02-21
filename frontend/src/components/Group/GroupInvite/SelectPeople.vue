<template>
  <div class="col-flex gap-1.5">
    <SelectPerson
      v-for="person in people"
      :key="person.id"
      :person="person"
      @click="$emit('chosen', person)"
      :isSelected="selected.has(person.id)"
    />
  </div>
</template>

<script>
import SelectPerson from "./SelectPerson.vue";
export default {
  props: {
    people: {
      type: Array,
      required: true,
    },
    selected: {
      type: Map,
      required: true,
    },
  },

  emits: ["chosen"],
  components: { SelectPerson },
};
</script>

<style scoped></style>
