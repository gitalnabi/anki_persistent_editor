function flipShowQuestion(q, bodyclass) {
  _updateQA(
    q,
    0 /* NOTE set to zero */,
    function () {
      // NOTE do not scroll
      // window.scrollTo(0, 0);

      document.body.className = bodyclass;
    },
    function () {
      // focus typing area if visible
      typeans = document.getElementById("typeans");
      if (typeans) {
        typeans.focus();
      }
    }
  );
}
