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

const mStore = useMediaStore();

document.addEventListener("keydown", (e) => {
  const component = mStore.currentMedia;
  if (!component) return;
  const { code } = e;
  const list = [code.toLowerCase()];
  e.ctrlKey && list.push("ctrl");
  switch (list.join(".")) {
    case "space":
      e.preventDefault();
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
  }
});
