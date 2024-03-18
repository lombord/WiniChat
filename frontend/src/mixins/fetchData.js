import abortController from "./abortController.js";

// Mixin to fetch data with pagination from the server
export default {
  data: () => ({
    /*
      Configuration properties
    */
    // axios request config object
    config: {},

    // if true data will be fetched when component is mounted
    mountFetch: true,
    // defines how scrolling should be handled when data is fetched
    reverseFetch: false,
    // Fetch limit for pagination
    limit: 15,

    /*
      Fetching properties. 
      Recommended not to change without knowing 
      what specific property does 
    */
    // defines if data is fetched
    loaded: false,
    // loaded data list
    dataList: [],
    // data range controllers
    prevOff: null,
    prevLimit: null,
    nextOff: null,
    nextLimit: null,

    // defines if data is being fetched
    fetchingPart: false,
  }),

  computed: {
    fetchElm() {
      const { fetchElm } = this.$refs;
      return fetchElm?.$el || fetchElm || this.$el;
    },

    fetchScroll() {
      return this.scrollElm || this.fetchElm;
    },

    previous() {
      const { prevOff } = this;
      if (prevOff != null) {
        return this.getFetchUrl({ offset: prevOff, limit: this.prevLimit });
      }
    },

    next() {
      const { nextOff } = this;
      if (nextOff != null) {
        return this.getFetchUrl({
          offset: nextOff,
          limit: this.nextLimit,
        });
      }
    },
  },

  async mounted() {
    if (this.mountFetch) {
      await this.fetchData();
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

    getFetchUrl(params) {
      params = params || {};
      if (!params.limit) params.limit = this.limit;
      let { pathname, searchParams } = new URL(
        this.fetchUrl,
        "http://localhost:5173"
      );
      Object.entries(params).forEach(([k, v]) => searchParams.set(k, v));
      pathname = pathname.replace(/^\/?api/, "");
      return `${pathname}?${searchParams}`;
    },

    getFetchParams(url) {
      const params = new URLSearchParams(new URL(url).searchParams);
      return [params.get("offset") || 0, params.get("limit")];
    },

    updatePrev(url) {
      if (!url) {
        this.prevOff = null;
        return;
      }
      [this.prevOff, this.prevLimit] = this.getFetchParams(url);
    },

    updateNext(url) {
      if (!url) {
        this.nextOff = null;
        return;
      }
      [this.nextOff, this.nextLimit] = this.getFetchParams(url);
    },

    async fetchData() {
      const { signal } = this.getNewController();
      let config = { signal };
      if (this.config) {
        config = { ...this.config, ...config };
      }
      const promise = this.$session.get(this.getFetchUrl(), config);
      try {
        const { data } = await this.$session.animate(promise, this.fetchElm);
        this.firstAdd(data.results || []);
        this.updatePrev(data.previous);
        this.updateNext(data.next);
      } catch (error) {
        console.log(error);
      }
    },

    /**
     * Called to fetch partial-data from given url config.
     */
    async fetchPart(url, cfg) {
      if (this.fetchingPart) return;
      this.fetchingPart = true;
      // await new Promise((r) => setTimeout(r, 101));
      const prom = this.$session.get(url, cfg);
      const response = await this.$session.animate(prom, 0, "xyz");
      this.fetchingPart = false;
      return response.data;
    },

    async _scrollTop() {
      const scrollElm = this.fetchScroll;
      const oldH = scrollElm.scrollHeight - scrollElm.clientHeight;
      const oldScroll = scrollElm.scrollTop;
      await this.$nextTick();
      const newH = scrollElm.scrollHeight - scrollElm.clientHeight;
      const diff = newH - oldH;
      requestAnimationFrame(() =>
        scrollElm.scrollTo({
          top: oldScroll + diff,
        })
      );
    },

    async _scrollBottom() {
      const scrollElm = this.fetchScroll;
      const { scrollTop } = scrollElm;
      await this.$nextTick();
      requestAnimationFrame(() => scrollElm.scrollTo({ top: scrollTop }));
    },

    /**
     * Called to signal to fetch the next url
     */
    async fetchNext() {
      if (!this.next) return true;
      const data = await this.fetchPart(this.next);
      if (!data) return;
      this.addNext(data.results);
      this.updateNext(data.next);
      this.reverseFetch ? this._scrollTop() : this._scrollBottom();
    },

    async fetchPrevious() {
      if (!this.previous) return true;
      const data = await this.fetchPart(this.previous);
      if (!data) return;
      this.addPrevious(data.results);
      this.updatePrev(data.previous);
      this.reverseFetch ? this._scrollBottom() : this._scrollTop();
    },
  },

  mixins: [abortController],
};
