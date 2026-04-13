// ============================================================
// 儿童口腔护理研究 — 站点交互脚本
// ============================================================

(function () {
  'use strict';

  // ---------- 主题切换 ----------
  const themeToggle = document.querySelector('.theme-toggle');
  const stored = localStorage.getItem('theme');
  if (stored) document.documentElement.setAttribute('data-theme', stored);

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const cur = document.documentElement.getAttribute('data-theme');
      const next = cur === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
      themeToggle.textContent = next === 'dark' ? '☀︎' : '☾';
    });
    const cur = document.documentElement.getAttribute('data-theme') ||
                (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    themeToggle.textContent = cur === 'dark' ? '☀︎' : '☾';
  }

  // ---------- 滚动进度条 ----------
  const progress = document.querySelector('.scroll-progress');
  if (progress) {
    window.addEventListener('scroll', () => {
      const h = document.documentElement;
      const scrolled = (h.scrollTop / (h.scrollHeight - h.clientHeight)) * 100;
      progress.style.width = scrolled + '%';
    }, { passive: true });
  }

  // ---------- 菜单切换(移动端) ----------
  const menuBtn = document.querySelector('.menu-toggle');
  const sidebar = document.querySelector('.sidebar');
  if (menuBtn && sidebar) {
    menuBtn.addEventListener('click', () => sidebar.classList.toggle('open'));
    document.addEventListener('click', (e) => {
      if (!sidebar.contains(e.target) && !menuBtn.contains(e.target)) {
        sidebar.classList.remove('open');
      }
    });
  }

  // ---------- 图片 lightbox ----------
  const lightbox = document.createElement('div');
  lightbox.className = 'lightbox';
  lightbox.innerHTML = '<img alt="">';
  document.body.appendChild(lightbox);

  document.querySelectorAll('.article img').forEach(img => {
    img.addEventListener('click', () => {
      lightbox.querySelector('img').src = img.src;
      lightbox.classList.add('active');
    });
  });
  lightbox.addEventListener('click', () => lightbox.classList.remove('active'));
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') lightbox.classList.remove('active');
  });

  // ---------- 表格响应式包装 ----------
  document.querySelectorAll('.article table').forEach(t => {
    if (t.parentElement.classList.contains('table-wrapper')) return;
    const wrap = document.createElement('div');
    wrap.className = 'table-wrapper';
    t.parentNode.insertBefore(wrap, t);
    wrap.appendChild(t);
  });

  // ---------- 客户端搜索 ----------
  const searchBox = document.getElementById('search-input');
  const searchResults = document.getElementById('search-results');
  let searchIndex = null;

  async function loadIndex() {
    if (searchIndex) return searchIndex;
    try {
      const res = await fetch('assets/search-index.json');
      searchIndex = await res.json();
    } catch (e) {
      console.error('Search index load failed:', e);
      searchIndex = [];
    }
    return searchIndex;
  }

  function escapeHTML(s) {
    return s.replace(/[&<>"']/g, c => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[c]));
  }

  function highlight(text, query) {
    const re = new RegExp('(' + query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
    return escapeHTML(text).replace(re, '<mark>$1</mark>');
  }

  async function runSearch(q) {
    if (!searchResults) return;
    q = q.trim();
    if (q.length < 2) {
      searchResults.innerHTML = '';
      return;
    }
    const idx = await loadIndex();
    const ql = q.toLowerCase();
    const results = [];

    for (const doc of idx) {
      const titleMatch = doc.title.toLowerCase().includes(ql);
      const contentIdx = doc.content.toLowerCase().indexOf(ql);
      if (titleMatch || contentIdx >= 0) {
        let snippet = '';
        if (contentIdx >= 0) {
          const start = Math.max(0, contentIdx - 40);
          const end = Math.min(doc.content.length, contentIdx + 120);
          snippet = (start > 0 ? '…' : '') + doc.content.slice(start, end) +
                    (end < doc.content.length ? '…' : '');
        }
        results.push({
          title: doc.title,
          path: doc.path,
          url: doc.url,
          snippet: snippet,
          score: (titleMatch ? 10 : 0) + (contentIdx >= 0 ? (5 - Math.min(5, contentIdx / 100)) : 0)
        });
      }
      if (results.length >= 30) break;
    }

    results.sort((a, b) => b.score - a.score);

    if (results.length === 0) {
      searchResults.innerHTML = '<div class="search-result">无匹配</div>';
      return;
    }

    searchResults.innerHTML = results.slice(0, 15).map(r =>
      '<a class="search-result" href="' + r.url + '">' +
      '<div class="search-result-title">' + escapeHTML(r.title) + '</div>' +
      '<div class="search-result-path">' + escapeHTML(r.path) + '</div>' +
      (r.snippet ? '<div class="search-result-snippet">' + highlight(r.snippet, q) + '</div>' : '') +
      '</a>'
    ).join('');
  }

  if (searchBox) {
    let timer = null;
    searchBox.addEventListener('input', (e) => {
      clearTimeout(timer);
      timer = setTimeout(() => runSearch(e.target.value), 150);
    });
  }

  // ---------- 右侧 TOC scrollspy(当前可见标题高亮)----------
  const tocRight = document.querySelector('.toc-right');
  if (tocRight) {
    const tocLinks = Array.from(tocRight.querySelectorAll('a[href^="#"]'));
    const headings = tocLinks
      .map(a => {
        const id = decodeURIComponent(a.getAttribute('href').slice(1));
        return { link: a, el: document.getElementById(id) };
      })
      .filter(h => h.el);

    if (headings.length > 0) {
      // 用 IntersectionObserver 做 scrollspy
      let activeLink = null;

      function setActive(link) {
        if (activeLink === link) return;
        if (activeLink) activeLink.classList.remove('active');
        if (link) link.classList.add('active');
        activeLink = link;

        // 自动滚动右栏让当前项可见
        if (link) {
          const tocBox = tocRight.getBoundingClientRect();
          const linkBox = link.getBoundingClientRect();
          if (linkBox.top < tocBox.top + 20 || linkBox.bottom > tocBox.bottom - 20) {
            link.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
          }
        }
      }

      // 手动计算最靠近顶部视口线(120px 下)的标题
      function updateActive() {
        const threshold = 120;
        let current = null;
        for (const h of headings) {
          const rect = h.el.getBoundingClientRect();
          if (rect.top - threshold <= 0) {
            current = h.link;
          } else {
            break;
          }
        }
        // 如果全都还在视口下方(文章顶部),高亮第一个
        if (!current && headings.length > 0) {
          const first = headings[0].el.getBoundingClientRect();
          if (first.top < window.innerHeight) current = headings[0].link;
        }
        setActive(current);
      }

      updateActive();
      window.addEventListener('scroll', updateActive, { passive: true });
      window.addEventListener('resize', updateActive);

      // 点击后平滑滚动(h2 的 offset 避开 48px topnav + 一点余量)
      tocLinks.forEach(a => {
        a.addEventListener('click', (e) => {
          e.preventDefault();
          const id = decodeURIComponent(a.getAttribute('href').slice(1));
          const el = document.getElementById(id);
          if (el) {
            const top = el.getBoundingClientRect().top + window.scrollY - 64;
            window.scrollTo({ top, behavior: 'smooth' });
            history.replaceState(null, '', '#' + id);
          }
        });
      });
    }
  }

  // ---------- 代码块添加 copy 按钮 ----------
  document.querySelectorAll('.article pre').forEach(pre => {
    const btn = document.createElement('button');
    btn.textContent = 'Copy';
    btn.style.cssText = 'position:absolute;top:8px;right:8px;padding:4px 10px;font-size:11px;border:none;background:var(--bg);color:var(--text-secondary);border-radius:6px;cursor:pointer;opacity:0;transition:opacity 0.2s;';
    pre.style.position = 'relative';
    pre.appendChild(btn);
    pre.addEventListener('mouseenter', () => btn.style.opacity = '1');
    pre.addEventListener('mouseleave', () => btn.style.opacity = '0');
    btn.addEventListener('click', () => {
      const code = pre.querySelector('code') || pre;
      navigator.clipboard.writeText(code.innerText).then(() => {
        btn.textContent = 'Copied';
        setTimeout(() => btn.textContent = 'Copy', 1500);
      });
    });
  });

})();
