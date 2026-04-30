#!/usr/bin/env node
/**
 * generate_docs.js — Gera PDF/DOCX/PPTX a partir dos MDs em docs/.
 *
 * Uso:
 *   node scripts/generate_docs.js              # processa todos os MDs em docs/**
 *   node scripts/generate_docs.js <arquivo.md> # processa apenas o arquivo
 *   node scripts/generate_docs.js --force      # regenera mesmo se output mais novo
 *
 * Convenções:
 *   - Espelha a estrutura de pastas: docs/<sub>/<nome>.md → docs/<sub>/generated/<nome>.{pdf,docx,pptx}
 *   - Nome do output = nome do MD com extensão trocada (1:1, sem flatten).
 *   - Arquivos em docs/<sub>/archive/ também são processados, saída em docs/<sub>/archive/generated/.
 *   - Formato por pasta:
 *       docs/dissemination/* com separadores `---` entre slides → PDF + PPTX
 *       docs/dissemination/* sem separadores                    → PDF + DOCX
 *       demais docs/<sub>/*                                     → PDF + DOCX
 *   - Incremental: só regenera se o MD for mais novo que o output (ou --force).
 */

const fs = require('fs');
const path = require('path');
const { marked } = require('marked');

const ROOT = path.resolve(__dirname, '..');
const DOCS_DIR = path.join(ROOT, 'docs');
const STYLE_FILE = path.join(ROOT, 'scripts', 'templates', 'styles', 'enterprise.css');

const args = process.argv.slice(2);
const FORCE = args.includes('--force');
const targetFile = args.find(a => !a.startsWith('--'));

// ---------- Markdown setup ----------

let hljs, katexExt;
try { hljs = require('highlight.js'); } catch { hljs = null; }
try { katexExt = require('marked-katex-extension'); } catch { katexExt = null; }

if (katexExt) marked.use(katexExt({ throwOnError: false }));

marked.use({
  renderer: {
    code(tokenOrCode, maybeLang) {
      // marked v14: arg is a token object {text, lang}; older: (code, lang)
      const code = typeof tokenOrCode === 'string' ? tokenOrCode : (tokenOrCode.text || '');
      const lang = typeof tokenOrCode === 'string' ? maybeLang : (tokenOrCode.lang || '');
      if (lang === 'mermaid') {
        return `<div class="mermaid">${escapeHtml(code)}</div>`;
      }
      if (hljs && lang && hljs.getLanguage(lang)) {
        const out = hljs.highlight(code, { language: lang }).value;
        return `<pre><code class="hljs language-${lang}">${out}</code></pre>`;
      }
      return `<pre><code>${escapeHtml(code)}</code></pre>`;
    },
  },
});

function escapeHtml(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// ---------- MD discovery ----------

function walkMarkdown(dir, out = []) {
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name === 'generated' || entry.name === 'assets') continue;
      walkMarkdown(full, out);
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      out.push(full);
    }
  }
  return out;
}

// ---------- Format routing ----------

function formatsFor(mdPath, rawMd) {
  const rel = path.relative(DOCS_DIR, mdPath).replace(/\\/g, '/');
  const isDissemination = rel.startsWith('dissemination/');
  const looksLikeSlides = isDissemination && /\n---\n/.test(rawMd);
  if (looksLikeSlides) return ['pdf', 'pptx'];
  return ['pdf', 'docx'];
}

function outputPathFor(mdPath, ext) {
  const dir = path.dirname(mdPath);
  const base = path.basename(mdPath, '.md');
  return path.join(dir, 'generated', `${base}.${ext}`);
}

function needsRegen(mdPath, outPath) {
  if (FORCE) return true;
  if (!fs.existsSync(outPath)) return true;
  return fs.statSync(mdPath).mtimeMs > fs.statSync(outPath).mtimeMs;
}

// ---------- TOC ----------

function buildToc(html) {
  const re = /<h([1-3])[^>]*>(.*?)<\/h\1>/g;
  const items = [];
  let m;
  let i = 0;
  const withIds = html.replace(re, (match, level, text) => {
    const id = `sec-${i++}`;
    items.push({ level: Number(level), text: stripTags(text), id });
    return `<h${level} id="${id}">${text}</h${level}>`;
  });
  if (items.length < 3) return { html: withIds, toc: '' };
  const lis = items
    .map(it => `<li class="level-${it.level}"><a href="#${it.id}">${it.text}</a></li>`)
    .join('');
  const toc = `<section class="toc"><h2>Sumário</h2><ul>${lis}</ul></section>`;
  return { html: withIds, toc };
}

function stripTags(s) {
  return s.replace(/<[^>]+>/g, '');
}

// ---------- HTML assembly ----------

function loadStyle() {
  if (fs.existsSync(STYLE_FILE)) return fs.readFileSync(STYLE_FILE, 'utf8');
  return '';
}

function buildHtml(mdPath, rawMd, { includeKatex = true, includeMermaid = true } = {}) {
  const css = loadStyle();
  const body = marked.parse(rawMd);
  const lineCount = rawMd.split('\n').length;
  const { html: bodyWithIds, toc } = lineCount > 100 ? buildToc(body) : { html: body, toc: '' };

  const relPath = path.relative(ROOT, mdPath).replace(/\\/g, '/');
  const title = path.basename(mdPath, '.md');
  const today = new Date().toISOString().slice(0, 10);

  const katexCss = includeKatex
    ? `<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">`
    : '';
  const mermaidScript = includeMermaid
    ? `<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
       <script>mermaid.initialize({ startOnLoad: true, theme: 'neutral' });</script>`
    : '';

  return `<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>${escapeHtml(title)}</title>
${katexCss}
<style>${css}</style>
</head>
<body>
<div class="content" data-source="${escapeHtml(relPath)}" data-generated="${today}">
${toc}
${bodyWithIds}
</div>
${mermaidScript}
</body>
</html>`;
}

// ---------- PDF ----------

async function renderPdf(browser, html, outPath, title) {
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'networkidle0' });
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  await page.pdf({
    path: outPath,
    format: 'A4',
    printBackground: true,
    margin: { top: '20mm', bottom: '20mm', left: '0', right: '0' },
    displayHeaderFooter: true,
    headerTemplate: `<div style="font-size:8pt;color:#888;width:100%;padding:0 20mm;">${escapeHtml(title)}</div>`,
    footerTemplate: `<div style="font-size:8pt;color:#888;width:100%;padding:0 20mm;display:flex;justify-content:space-between;">
      <span>${new Date().toISOString().slice(0, 10)}</span>
      <span><span class="pageNumber"></span> / <span class="totalPages"></span></span>
    </div>`,
  });
  await page.close();
}

// ---------- DOCX ----------

async function renderDocx(html, outPath) {
  let htmlDocx;
  try { htmlDocx = require('html-docx-js'); } catch {
    console.warn(`  ⚠ html-docx-js não instalado — pulando DOCX`);
    return false;
  }
  const blob = htmlDocx.asBlob(html);
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  // asBlob pode retornar Buffer (Node antigo) ou Blob (Node 18+). Normaliza.
  let data;
  if (Buffer.isBuffer(blob)) data = blob;
  else if (typeof blob.arrayBuffer === 'function') data = Buffer.from(await blob.arrayBuffer());
  else data = Buffer.from(blob);
  fs.writeFileSync(outPath, data);
  return true;
}

// ---------- PPTX ----------

async function renderPptx(rawMd, outPath, title) {
  let PptxGenJS;
  try { PptxGenJS = require('pptxgenjs'); } catch {
    console.warn(`  ⚠ pptxgenjs não instalado — pulando PPTX`);
    return false;
  }
  const pptx = new PptxGenJS();
  pptx.title = title;
  const slides = rawMd.split(/\n---\n/);
  for (const slideMd of slides) {
    const slide = pptx.addSlide();
    const headingMatch = slideMd.match(/^\s*#{1,3}\s+(.+)$/m);
    const heading = headingMatch ? headingMatch[1].trim() : '';
    const body = slideMd.replace(/^\s*#{1,3}\s+.+$/m, '').trim();
    if (heading) slide.addText(heading, { x: 0.5, y: 0.3, w: 9, h: 0.8, fontSize: 28, bold: true, color: '2c3e6b' });
    if (body) slide.addText(body, { x: 0.5, y: 1.3, w: 9, h: 5.5, fontSize: 14, valign: 'top' });
  }
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  await pptx.writeFile({ fileName: outPath });
  return true;
}

// ---------- Main ----------

async function main() {
  const files = targetFile
    ? [path.resolve(targetFile)]
    : walkMarkdown(DOCS_DIR);

  if (files.length === 0) {
    console.log('Nenhum .md encontrado em docs/.');
    return;
  }

  let puppeteer;
  try { puppeteer = require('puppeteer'); } catch {
    console.error('Erro: puppeteer não instalado. Rode `npm install` na raiz do projeto.');
    process.exit(1);
  }
  const browser = await puppeteer.launch({ args: ['--no-sandbox'] });

  let built = 0, skipped = 0;
  for (const mdPath of files) {
    const raw = fs.readFileSync(mdPath, 'utf8');
    const formats = formatsFor(mdPath, raw);
    const title = path.basename(mdPath, '.md');
    const html = buildHtml(mdPath, raw);
    const rel = path.relative(ROOT, mdPath).replace(/\\/g, '/');

    for (const fmt of formats) {
      const out = outputPathFor(mdPath, fmt);
      if (!needsRegen(mdPath, out)) { skipped++; continue; }
      try {
        if (fmt === 'pdf') await renderPdf(browser, html, out, title);
        else if (fmt === 'docx') await renderDocx(html, out);
        else if (fmt === 'pptx') await renderPptx(raw, out, title);
        console.log(`✓ ${rel} → ${path.relative(ROOT, out).replace(/\\/g, '/')}`);
        built++;
      } catch (err) {
        console.error(`✗ ${rel} (${fmt}): ${err.message}`);
      }
    }
  }

  await browser.close();
  console.log(`\n${built} gerado(s), ${skipped} pulado(s).`);
}

main().catch(err => { console.error(err); process.exit(1); });
