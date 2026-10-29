# Механічний рух

One interactive Ukrainian HTML/JavaScript page containing all 16 exercises and the full worked solutions from the reviewed PDF. Includes topic filters, full-text search, collapsible solutions, direct exercise links, print support, and a red river-motion reference rule. Tables preserve the PDF's Дано / СІ / Розв’язання structure; СІ appears only where needed.

## Preview

```sh
python3 -m http.server 8000
```

Open http://localhost:8000. Mathematical notation is rendered with MathJax 3.2.2 from jsDelivr (internet required). No application build or framework is required to serve the committed page.

## Update content

Edit `exercises.tex`, then run `python3 build.py`. This regenerates `index.html` from the same LaTeX source as the PDF, preserving all problem statements, derivations, and answers. When updating the PDF, compile the source with XeLaTeX and save it as `exercises.pdf` (Times New Roman required).

## GitHub Pages

In repository Settings → Pages, choose **Deploy from a branch**, branch **main**, folder **/(root)**. The committed `index.html` is the entry point. `.nojekyll` keeps this a plain static website.
