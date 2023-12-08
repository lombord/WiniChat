<template>
  <div>
    <div class="main-div">
      <div
        class="menu-box"
        @mouseenter="showMenu = true"
        @mouseleave="showMenu = false"
      >
        <PhotoEdit class="photo-edit" />
        <ContextMenu class="context" v-model:show="showMenu" :menu="menu">
          <template #theme>
            <span class="theme-icon dark" v-if="theme == 'light'">
              <i class="fa-solid fa-moon"></i>
              <span class="menu-label"> Dark </span>
            </span>
            <span class="theme-icon light" v-else>
              <i class="fa-solid fa-sun"></i>
              <span class="menu-label"> Light </span>
            </span>
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
      <div class="flex-1 truncate z-[100]">
        <h5 class="text-primary">{{ name }}</h5>
        <p class="text-base-content/80 flex font-bold gap-0.5">
          <span class="text-secondary">
            <i class="fa-solid fa-at"></i>
          </span>
          {{ user.username }}
        </p>
      </div>
    </div>
    <Settings v-model:show="showSettings" />
  </div>
</template>

<script>
import PhotoEdit from "@/components/user/PhotoEdit.vue";
import ContextMenu from "@/components/UI/ContextMenu.vue";
import Settings from "@/components/user/Settings.vue";

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
  @apply flex items-center gap-2
  relative md:gap-3;
}

:deep(.photo-edit) {
  @apply md:w-20 relative z-[100];
}

.context {
  @apply -top-2 -left-2 pt-16
  md:pt-24 w-full max-w-sm;
}

.menu-label {
  @apply text-sm align-middle hidden md:inline;
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

<style>
.context *[contextId] {
  @apply py-3 text-xl;
}

.context *[contextId="theme"] {
  @apply py-2.5;
}
</style>
