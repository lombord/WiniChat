export default {
  data: () => ({
    fetchController: null,
  }),

  methods: {
    getNewController(timeout = 5000) {
      let controller = this.fetchController;
      if (controller && !controller.signal.aborted) {
        controller.abort();
      }

      controller = this.fetchController = new AbortController();

      const tId = setTimeout(() => {
        if (!controller.signal.aborted) {
          controller.abort("abort cancel");
        }
      }, timeout);

      controller.signal.addEventListener("abort", () => {
        clearTimeout(tId);
      });

      return controller;
    },
  },
};
