// Global store for media files

import { defineStore } from "pinia";

export const useMediaStore = defineStore("media", {
  state: () => ({
    volume: 30,
    currentMedia: null,
    muted: false,
  }),
  getters: {},
  actions: {},
});

document.addEventListener("keydown", (e) => {
  const mStore = useMediaStore();
  const component = mStore.currentMedia;
  if (!component || document.activeElement != document.body) return;
  const rect = component.$el.getBoundingClientRect();
  if (!(rect.width && rect.height)) return;
  let hasAny = true;
  const { code } = e;
  const list = [code.toLowerCase()];
  e.ctrlKey && list.push("ctrl");
  switch (list.join(".")) {
    case "space":
      component.toggleState();
      break;
    case "keyf":
      try {
        component.toggleFullScreen();
      } catch (err) {}
      break;
    case "keym":
      component.toggleMute();
      break;
    case "arrowleft":
      component.rewind(-5);
      break;
    case "arrowright":
      component.rewind(5);
      break;
    case "arrowup.ctrl":
      component.volume += 5;
      break;
    case "arrowdown.ctrl":
      component.volume -= 5;
      break;
    default:
      hasAny = false;
      break;
  }
  if (hasAny) {
    e.stopPropagation();
    e.preventDefault();
  }
});
