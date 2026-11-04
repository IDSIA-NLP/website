// Filter publications by theme and by free text. No libraries needed.
(function () {
  var buttons = document.querySelectorAll('.filter');
  var search = document.getElementById('pub-search');
  var theme = '';
  function apply() {
    var q = (search.value || '').toLowerCase().trim();
    var shown = 0;
    document.querySelectorAll('.year-group').forEach(function (g) {
      var n = 0;
      g.querySelectorAll('.pub').forEach(function (p) {
        var okTheme = !theme || (' ' + p.dataset.themes + ' ').indexOf(' ' + theme + ' ') >= 0;
        var okText = !q || p.textContent.toLowerCase().indexOf(q) >= 0;
        p.hidden = !(okTheme && okText);
        if (!p.hidden) n++;
      });
      g.hidden = n === 0;
      shown += n;
    });
    document.getElementById('pub-empty').hidden = shown > 0;
  }
  buttons.forEach(function (b) {
    b.addEventListener('click', function () {
      buttons.forEach(function (x) { x.classList.remove('is-active'); });
      b.classList.add('is-active');
      theme = b.dataset.theme;
      apply();
    });
  });
  search.addEventListener('input', apply);
})();
