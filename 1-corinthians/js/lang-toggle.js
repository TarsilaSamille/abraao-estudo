// Shared across all sessions. Bilingual toggle. Preserves the page's own
// lang code format (e.g. "pt-BR" vs "pt") so the html[lang=...] CSS rules
// that hide the inactive language keep matching. A stale saved value in the
// wrong format (left by older builds) is ignored.
(function () {
  var declared = document.documentElement.getAttribute('lang') || 'pt';
  window.__ptForm = declared.split('-')[0] === 'pt' ? declared : 'pt';
})();

function setLang(lang) {
  var target = (lang === 'en' || lang === 'en-US' || lang === 'en-GB') ? 'en' : window.__ptForm;
  document.documentElement.setAttribute('lang', target);
  var m = location.pathname.match(/sessao-(\d+)/);
  var key = m ? 's' + m[1] + '-lang' : 'session-lang';
  try { localStorage.setItem(key, target); } catch (e) {}
  var pt = document.getElementById('lang-pt'), en = document.getElementById('lang-en');
  if (!pt || !en) return;
  if (target === 'en') {
    en.className = "px-3.5 py-1.5 text-sm font-semibold transition-colors bg-sky-600 text-white rounded-r-full";
    pt.className = "px-3.5 py-1.5 text-sm font-semibold transition-colors bg-white text-slate-600 hover:bg-slate-50 rounded-l-full";
  } else {
    pt.className = "px-3.5 py-1.5 text-sm font-semibold transition-colors bg-sky-600 text-white rounded-l-full";
    en.className = "px-3.5 py-1.5 text-sm font-semibold transition-colors bg-white text-slate-600 hover:bg-slate-50 rounded-r-full";
  }
}

(function () {
  var ptForm = window.__ptForm || 'pt';
  var m = location.pathname.match(/sessao-(\d+)/);
  var key = m ? 's' + m[1] + '-lang' : 'session-lang';
  var saved = null;
  try { saved = localStorage.getItem(key); } catch (e) {}
  var valid = saved === 'en' || saved === ptForm;
  var declared = document.documentElement.getAttribute('lang') || 'pt';
  setLang(valid ? saved : declared);
})();
