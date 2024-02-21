<template>
  <div v-if="canAdd" class="relative col-flex max-h-[inherit] overflow-hidden">
    <SearchFetch :url="inviteUrl">
      <template #inBetween>
        <div class="shrink-0">
          <Transition name="pop" mode="out-in">
            <Bubbles
              v-if="selected.size"
              :people="selected"
              @remove="removeItem"
              @clear="clearSelected"
            />
            <p v-else class="bubble-placeholder">Choose people</p>
          </Transition>
        </div>
      </template>
      <template #fetched="{ dataList }">
        <SelectPeople
          :people="dataList"
          class="flex-1 pb-1 overflow-y-auto"
          :selected="selected"
          @chosen="toggleItem"
        />
      </template>
      <template #noResult>
        <h2 class="text-secondary text-center">
          <i class="bi bi-person-fill-x"></i>
        </h2>
      </template>
    </SearchFetch>

    <div class="buttons-box">
      <Transition name="pop">
        <button
          v-if="selected.size"
          @click="inviteMembers"
          class="btn invite-btn spinner-on-load center-content"
        >
          <i class="fa-solid fa-plus"></i>
        </button>
      </Transition>
    </div>
  </div>
</template>

<script>
import SearchFetch from "@/components/Fetch/SearchFetch.vue";
import accessRequired from "../GroupRoles/accessRequired.js";

import SelectPeople from "./SelectPeople.vue";
import Bubbles from "./Bubbles.vue";

export default {
  data: () => ({
    accessPerm: "add_user",
    selected: new Map(),
  }),

  props: {
    group: {
      type: Object,
      required: true,
    },
  },

  computed: {
    url() {
      return this.group.url;
    },

    role() {
      return this.group.user_role;
    },

    inviteUrl() {
      return `${this.url}invites/`;
    },
  },

  deactivated() {
    this.selected?.clear();
  },

  methods: {
    async inviteMembers({ currentTarget: elm }) {
      const people = Array.from(this.selected.keys());
      if (!(this.canAdd && people)) return;
      try {
        const session = this.$session;
        const prom = session.post(`${this.url}members/`, { users: people });
        const { data } = await session.animate(prom, elm);
        const group_id = this.group.id;
        session.socket.groupMessage("new_members", { group_id, data });
        session.socket.sendGroupEvent({
          event: "invite",
          group_id,
          members: data,
        });
        this.selected.clear();
        this.$emit("invited", data);
      } catch (err) {
        this.$flashes.axiosError(err);
      }
    },

    toggleItem(person) {
      if (this.selected.has(person.id)) {
        this.selected.delete(person.id);
      } else {
        this.selected.set(person.id, person);
      }
    },

    removeItem(person) {
      this.selected.delete(person.id);
    },

    clearSelected() {
      this.selected.clear();
    },
  },

  emits: ["invited"],
  components: { SearchFetch, SelectPeople, Bubbles },
  mixins: [accessRequired],
};
</script>

<style scoped>
.bubble-placeholder {
  @apply p-1.5 text-white/90 rounded-full font-bold 
  text-center text-lg bg-primary-medium;
}

.buttons-box {
  @apply absolute bottom-0 p-3 pointer-events-none
  inset-x-0 flex justify-end gap-2;
}

.buttons-box > * {
  @apply pointer-events-auto;
}

.invite-btn {
  @apply btn-primary rounded-full aspect-square text-4xl p-4;
}
</style>
