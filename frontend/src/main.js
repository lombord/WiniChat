import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "@/App.vue";
import router from "@/router";
import directives from "@/directives";
import defineGlobals from "@/plugins/defineGlobals.js";
import { request } from "@/plugins/request.js";

// pass loadRouter function to give RootComponent
// opportunity to load router when it is ready
const app = createApp(App, {
  loadRouter: () => app.use(router),
});

app.use(createPinia());

const { useSessionStore } = await import("@/stores/session.js");
const { useFlashesStore } = await import("@/stores/flashes.js");
const { useMediaStore } = await import("@/stores/media.js");
const { useTracksStore } = await import("@/stores/tracks.js");

const sessionStore = useSessionStore();

// list of global plugins
const globalPlugins = [
  { name: "request", value: request },
  { name: "session", value: sessionStore },
  { name: "flashes", value: useFlashesStore() },
  { name: "media", value: useMediaStore() },
  { name: "tracks", value: useTracksStore() },
];

app.use(defineGlobals, globalPlugins);

app.provide("session", sessionStore);

directives.forEach((dir) => app.directive(dir.name, dir));

app.mount("#app");
