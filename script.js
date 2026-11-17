document.querySelectorAll('.math').forEach((element) => {
  if (window.katex) {
    window.katex.render(element.dataset.tex, element, { displayMode: true, throwOnError: false });
  }
});
