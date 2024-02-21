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

// pass loadRouter function to give RootComponent
// opportunity to load router when it is ready
const app = createApp(App, {
  loadRouter: () => app.use(router),
});

app.use(createPinia());

// Global store imports
const { useSessionStore } = await import("@/stores/session.js");
const { useFlashesStore } = await import("@/stores/flashes.js");
const { useUtilsStore } = await import("@/stores/utils.js");
const { useProfileStore } = await import("@/stores/profile.js");
const { useChatsStore } = await import("@/stores/chats.js");
const { useGroupStore } = await import("@/stores/group.js");
const { useMediaStore } = await import("@/stores/media.js");
const { useTracksStore } = await import("@/stores/tracks.js");

const sessionStore = useSessionStore();

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
