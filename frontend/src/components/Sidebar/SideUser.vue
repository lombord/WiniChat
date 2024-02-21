<template>
  <div>
    <div
      class="main-div"
      @mouseenter="showMenu = true"
      @mouseleave="showMenu = false"
    >
      <PhotoEdit class="photo-edit" />
      <div class="flex-1 truncate z-[100]">
        <h5 class="text-primary-light">{{ name }}</h5>
        <IdTag>
          {{ user.username }}
        </IdTag>
      </div>
      <ContextMenu class="context" v-model:show="showMenu" :menu="menu">
        <template #theme>
          <template v-if="theme == 'light'">
            <i class="fa-solid fa-moon theme-icon dark"></i>
            <span class="menu-label theme-icon dark"> Dark </span>
          </template>
          <template v-else>
            <i class="fa-solid fa-sun theme-icon light"></i>
            <span class="menu-label theme-icon light"> Light </span>
          </template>
        </template>
        <template #settings>
          <i class="fa-solid fa-gear"></i>
          <span class="menu-label">Settings</span>
        </template>
        <template #logout>
          <i class="fa-solid fa-right-from-bracket"></i>
          <span class="menu-label">Logout</span>
        </template>
      </ContextMenu>
    </div>
    <Settings v-if="showSettings" v-model:show="showSettings" />
  </div>
</template>

<script>
import PhotoEdit from "@/components/User/PhotoEdit.vue";
import ContextMenu from "@/components/UI/ContextMenu.vue";
import Settings from "@/components/User/Settings.vue";

export default {
  data: () => ({
    showMenu: false,
    showSettings: false,
    theme: null,
  }),

  computed: {
    user() {
      return this.$session.user;
    },

    name() {
      return this.user.full_name || this.user.username;
    },

    menu() {
      return [
        {
          label: "theme",
          cb: this.switchTheme,
        },
        {
          label: "settings",
          cb: () => (this.showSettings = true),
        },

        {
          label: "logout",
          cb: this.logout,
        },
      ];
    },
  },

  created() {
    this.theme = localStorage.getItem("theme") || "light";
  },

  methods: {
    logout() {
      this.$router.push({ name: "logout" });
    },

    switchTheme() {
      this.theme == "light" ? (this.theme = "dark") : (this.theme = "light");
    },
  },

  watch: {
    theme(val) {
      const rootElm = document.documentElement;
      rootElm.setAttribute("data-theme", val);
      localStorage.setItem("theme", val);
    },
  },

  components: { PhotoEdit, ContextMenu, Settings },
};
</script>

<style scoped>
.main-div {
  @apply flex items-center gap-3
  relative md:gap-4 pl-1 pb-1;
}

:deep(.photo-edit) {
  @apply md:w-20 relative z-[100];
}

.context {
  @apply -top-2 -left-1 pt-[6.3em] w-full max-w-sm;
}

.context :deep(.menu-btn) {
  @apply text-xl py-2.5;
}

.menu-label {
  @apply text-base align-middle hidden md:inline capitalize;
}

.theme-icon.light {
  @apply text-yellow-300;
}

.theme-icon.dark {
  @apply text-primary;
}

.logout-btn {
  @apply opacity-30 hover:opacity-100 
  hover:btn-primary text-xl py-2;
}
</style>
