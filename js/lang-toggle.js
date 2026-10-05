// Bilingual toggle, shared by every session (all 442 pages load this via
// "../../js/lang-toggle.js", which resolves to the /js/ folder at the repo
// root).
//
// Storage: ONE global key, "bp_lang". The 442 inline scripts also write
// "bp_lang", so the two agree.
//
// This file used to key on "lang-" + location.pathname — one entry per page.
// Two problems came out of that:
//   1. the choice did not follow you across the site (page A in PT, page B in
//      EN), which is what "the default is always English" felt like;
//   2. because this file loads AFTER the inline <script>, its global setLang
//      shadowed the inline one, so the inline "bp_lang" logic was dead code and
//      the per-page key was the only thing in charge — a page you had once
//      toggled stayed toggled forever.
// The legacy per-page keys are purged below so anyone already stuck that way
// starts clean at PT.
//
// Buttons call setLang('pt'|'en') via inline onclick, so setLang must stay
// global. The PT form is taken from the page's initial <html lang> (some pages
// declare "pt-BR"), never from the live attribute, which flips to "en" on
// toggle.
(function () {
  var declared = document.documentElement.getAttribute('lang') || 'pt';
  window.__ptForm = declared.split('-')[0] === 'pt' ? declared : 'pt';

  // Purge the old per-page keys so stale English choices stop applying.
  try {
    var legacy = [];
    for (var i = 0; i < localStorage.length; i++) {
      var k = localStorage.key(i);
      if (k && k.indexOf('lang-') === 0) legacy.push(k);
    }
    for (var j = 0; j < legacy.length; j++) localStorage.removeItem(legacy[j]);
  } catch (e) {}
})();

function setLang(lang) {
  var isEn = (lang === 'en' || lang === 'en-US' || lang === 'en-GB');
  // The attribute keeps each page's own PT form ("pt" or "pt-BR"), so the
  // html[lang^="pt"] CSS rules keep matching. Storage always gets the short
  // canonical form, otherwise a pt-BR page (atos-dos-apostolos) would write
  // "pt-BR" and every pt page opened afterwards would inherit it.
  var target = isEn ? 'en' : window.__ptForm;
  document.documentElement.setAttribute('lang', target);
  try { localStorage.setItem('bp_lang', isEn ? 'en' : 'pt'); } catch (e) {}
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
  var saved = null;
  try { saved = localStorage.getItem('bp_lang'); } catch (e) {}
  // Accept "pt" and "pt-BR" alike, so a value written by a pt-BR page still
  // reads correctly on a pt page and vice-versa. Anything else (including a
  // null, i.e. a first visit) falls back to Portuguese.
  var isEn = saved === 'en';
  var isPt = typeof saved === 'string' && saved.split('-')[0] === 'pt';
  setLang(isEn ? 'en' : isPt ? ptForm : 'pt');
})();