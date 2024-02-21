<template>
  <div class="flex flex-col gap-1" :class="$attrs.class">
    <TransitionGroup name="item-down">
      <Member
        v-bind="$utils.exclude($attrs, ['class'])"
        v-for="member in members"
        :key="member.id"
        :member="member"
      />
    </TransitionGroup>
  </div>
</template>

<script>
import Member from "./Member.vue";

export default {
  props: {
    members: {
      required: true,
    },
  },

  components: { Member },
  inheritAttrs: false,
};
</script>
