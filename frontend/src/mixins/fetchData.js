// Mixin to fetch data with pagination from the server
export default {
  data: () => ({
    // request config
    config: {},
    // defines if data is fetched
    loaded: false,
    // loaded data list
    dataList: [],
    // previous page url
    previous: null,
    // next page url
    next: null,
    // defines if data is being fetched
    _fetching: false,
    // if true data will be fetched when component is mounted
    fetch_on_mounted: true,
    // AbortController controller object
    controller: null,
  }),

  computed: {
    fetchElm() {
      return this.$refs.fetchElm;
    },
  },

  mounted() {
    if (this.fetch_on_mounted) {
      this.fetchData();
    }
    this.loaded = true;
  },

  methods: {
    firstAdd(data) {
      this.dataList = data || [];
    },

    addNext(data) {
      this.dataList.push(...data);
    },

    addPrevious(data) {
      this.dataList.unshift(...data);
    },

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
        const { data } = await this.$session.animate(promise, this.fetchElm);
        this.firstAdd(data.results);
        this.previous = data.previous;
        this.next = data.next;
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
     * Called to fetch partial-data from given url config.
     */
    async fetchPart(url, cfg) {
      if (this._fetching) return;
      this._fetching = true;
      // await new Promise((r) => setTimeout(r, 1000));
      const prom = this.$session.get(url, cfg);
      const response = await this.$session.animate(prom, 0, "xyz");
      this._fetching = false;
      return response.data;
    },

    /**
     * Called to signal to fetch the next url
     */
    async loadNext(el) {
      if (!this.next) return true;
      const { results, next } = await this.fetchPart(this.next);
      this.addNext(results);
      this.next = next;
      await this.$nextTick();
      this.fetchElm.scrollTo({
        top: this.fetchElm.scrollTop + el.offsetHeight + 10,
      });
    },

    async loadPrevious() {
      if (!this.previous) return true;
      const { results, previous } = await this.fetchPart(this.previous);
      const { scrollTop } = this.fetchElm;
      this.addPrevious(results);
      this.previous = previous;
      await this.$nextTick();
      this.fetchElm.scrollTo({ top: scrollTop });
    },
  },
};
