// Directive for tracking interaction of an element
export default {
  name: "int",
  mounted(el, { value }) {
    function callback([entry], observer) {
      if (!entry.isIntersecting) return;
      const stop = value(el, entry);
      // if true, stop tracking and hide the element
      if (stop) {
        el.classList.add("hidden");
        observer.unobserve(el);
      }
    }
    const observer = new IntersectionObserver(callback);
    observer.observe(el);
  },
};
