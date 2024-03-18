import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "@/App.vue";
import router from "@/router";
import directives from "@/directives";
import defineGlobals from "@/plugins/defineGlobals.js";
import { request } from "@/plugins/request.js";
import ImgAnim from "@/components/Media/Images/ImgAnim.vue";
import FetchObserver from "@/components/Fetch/FetchObserver.vue";
import IdTag from "@/components/UI/IdTag.vue";
import IconTag from "@/components/UI/IconTag.vue";

// Global store imports
import { useSessionStore } from "@/stores/session.js";
import { useFlashesStore } from "@/stores/flashes.js";
import { useUtilsStore } from "@/stores/utils.js";
import { useProfileStore } from "@/stores/profile.js";
import { useChatsStore } from "@/stores/chats.js";
import { useGroupStore } from "@/stores/group.js";
import { useMediaStore } from "@/stores/media.js";
import { useTracksStore } from "@/stores/tracks.js";

// pass loadRouter function to give RootComponent
// opportunity to load router when it is ready
const app = createApp(App, {
  loadRouter: () => app.use(router),
});

app.use(createPinia());

const sessionStore = useSessionStore();

sessionStore.$subscribe((mutation, state) => {
  if (!state) return;
  const { access, refresh } = state;
  access && localStorage.setItem("access", state.access);
  refresh && localStorage.setItem("refresh", state.refresh);
});

// list of global plugins
const globalPlugins = [
  { name: "request", value: request },
  { name: "session", value: sessionStore },
  { name: "flashes", value: useFlashesStore() },
  { name: "utils", value: useUtilsStore() },
  { name: "media", value: useMediaStore() },
  { name: "tracks", value: useTracksStore() },
  { name: "profile", value: useProfileStore() },
  { name: "chats", value: useChatsStore() },
  { name: "group", value: useGroupStore() },
];
app.use(defineGlobals, globalPlugins);

app.provide("session", sessionStore);

app.component("ImgAnim", ImgAnim);
app.component("FetchObserver", FetchObserver);
app.component("IdTag", IdTag);
app.component("IconTag", IconTag);
directives.forEach((dir) => app.directive(dir.name, dir));

app.mount("#app");
