// Mixin to fetch data with pagination from the server
export default {
  data: () => ({
    // request config
    config: {},
    // defines if data is fetched
    loaded: false,
    // loaded data list
    dataList: [],
    // next page url
    next: null,
    // defines if data is being fetched
    _fetching: false,
    // if true data will be fetched when component is mounted
    fetch_on_mounted: true,
    // AbortController controller object
    controller: null,
  }),

  mounted() {
    if (this.fetch_on_mounted) {
      this.fetchData();
    }
    this.loaded = true;
  },

  methods: {
    /**
     * Base fetch function, fetches data from defined url
     * and updates dataList by fetched data.
     * Called when a url is fetched for the first time
     */
    async fetchData() {
      this.controller = this.getController();
      let config = { signal: this.controller.signal };
      if (this.config) {
        config = { ...this.config, ...config };
      }
      const promise = this.$session.get(this.url, config);
      try {
        const response = await this.$session.animate(
          promise,
          this.$refs.fetchElm
        );
        this.dataList = [];
        this.update(response.data);
      } catch (error) {}
    },

    /**
     * Creates AbortController based on timeout.
     * @param {Number} timeout - timeout in millisecond.
     * @return {AbortController} AbortController instance.
     */
    getController(timeout = 5000) {
      const controller = new AbortController();
      setTimeout(() => {
        if (!controller.signal.aborted) {
          controller.abort();
        }
      }, timeout);
      return controller;
    },

    /**
     * Called when dataList is being extended with a new data.
     */
    update({ results, next }) {
      const len = this.dataList.length;
      this.dataList.push(...results);
      if (this.addCallback) {
        this.dataList.slice(len).forEach(this.addCallback);
      }
      this.next = next;
    },

    /**
     * Called to fetch a next url.
     */
    async loadNext() {
      if (this._fetching) return;
      this._fetching = true;
      const cfg = { url: this.next, baseURL: "" };
      const prom = this.$session.request(cfg);
      const response = await this.$session.animate(prom, 0, "xyz");
      this.update(response.data);
      this._fetching = false;
    },

    /**
     * Called to signal to fetch the next url
     */
    intersected() {
      if (!this.next) return true;
      this.loadNext();
    },
  },
};
