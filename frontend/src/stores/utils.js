// Global store for utility tools

import { defineStore } from "pinia";
import { markRaw, defineComponent, defineAsyncComponent } from "vue";

export const useUtilsStore = defineStore("utils", {
  state: () => ({
    cachedComps: markRaw(new Map()),
    fetchingComps: markRaw(new Map()),
  }),

  actions: {
    // dynamic import related actions
    dynImport(path) {
      return defineAsyncComponent(() => this.dynLoader(path));
    },

    async compImport(path) {
      const comp = await this.dynLoader(path);
      return defineComponent(markRaw(comp.default));
    },

    async dynLoader(path) {
      const { cachedComps } = this;
      let component = cachedComps.get(path);
      if (!component) {
        const { fetchingComps } = this;
        let prom = fetchingComps.get(path);
        if (!prom) {
          prom = import(/* @vite-ignore */ `/src/components/${path}`);
          fetchingComps.set(path, prom);
          component = await prom;
          fetchingComps.delete(path);
        } else {
          component = await prom;
        }
        cachedComps.set(path, component);
      }
      return component;
    },

    // common actions
    exclude(obj, exc) {
      exc = new Set(exc);
      return Object.fromEntries(
        Object.entries(obj).filter(([key]) => !exc.has(key))
      );
    },

    randInt(a = 0, b = 0) {
      if (!b) {
        (b = a), (a = 0);
      }
      return Math.floor(Math.random() * (b - a) + a);
    },

    range(val, min, max) {
      return Math.max(min, Math.min(val, max));
    },

    wait(ms) {
      return new Promise((r) => setTimeout(r, ms));
    },

    async waitProm(promise, ms) {
      await this.wait(ms);
      return await promise;
    },

    formatBytes(bytes, decimals = 2) {
      if (!+bytes) return "0B";
      const k = 1024;
      const dm = decimals < 0 ? 0 : decimals;
      const sizes = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))}${sizes[i]}`;
    },
  },
});
