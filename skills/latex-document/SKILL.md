---
name: latex-document
description: >
  Create, edit, and compile LaTeX source files (.tex) for academic papers,
  reports, theses, and presentations. Produces publication-ready PDFs via
  pdflatex or xelatex.
skills: []
tools: Read, Write, Bash
---

# LaTeX Document Skill

Write clean, compilable LaTeX. Prefer semantic markup and standard packages. This skill covers creating new documents, editing existing ones, and troubleshooting compilation errors.

Source: `latex2e.pdf` unofficial reference manual (https://texdoc.org/serve/latex2e.pdf/0)

## When to Use

- The user asks for a PDF document, paper, report, or CV
- Refactoring or fixing compilation errors in `.tex` files
- Adding figures, tables, or equations to an existing document
- Converting a markdown manuscript to LaTeX for journal submission

## Principles

1. **Start from a minimal working example.** Do not add packages unless required. Every package increases compilation time and potential for conflict.
2. **Semantic markup.** Use `\section`, `\emph`, `\label`/`\ref` instead of manual formatting. This makes the document maintainable and portable.
3. **One sentence per line** in the `.tex` source. This keeps diffs readable and makes debugging easier.
4. **Never hardcode paths.** Use relative paths for `\includegraphics` and `\input`.
5. **Use `\input` for sections.** Split the document into `sections/` directory with one file per section. Keep the main `.tex` file as a skeleton.
6. **Compile with `latexmk`** if available. It handles multiple passes (bibtex, glossary, etc.) automatically.

## Selecting a Reference File

When the task matches a row in the table below, **read the corresponding reference file** from `skills/latex-document/references/` to get the full details. The reference files contain templates, package options, and examples extracted from the `latex2e.pdf` manual.

| If the task involves... | Read this reference | Contents |
|---|---|---|
| Choosing a document class (article, book, report, beamer, letter) | `references/templates.md` | All templates with options |
| Font selection, sizes, families, math fonts | `references/fonts.md` | NFSS, fontenc, fontspec, math fonts |
| Page layout, margins, columns | `references/layout.md` | \onecolumn, geometry, \setlength |
| Sectioning, TOC, appendix | `references/sectioning.md` | \section through \subparagraph, tocdepth |
| Cross-references, labels, cleveref | `references/cross-references.md` | \label, \ref, \pageref, \autoref |
| Environments (itemize, enumerate, minipage, verbatim, etc.) | `references/environments.md` | All important environments |
| Line breaks, page breaks, footnotes, spacing, lengths | `references/spacing.md` | \\, \newpage, \footnote, \setlength, \hspace |
| Math formulas, symbols, matrices, equations | `references/math.md` | amsmath, \frac, \begin{align}, Greek letters |
| Graphics, color, boxes | `references/graphics-color.md` | \includegraphics, \textcolor, \fbox, \parbox |
| Special characters, accents, dashes, quotes | `references/special-characters.md` | Reserved chars, accents, \textcopyright, \today |
| Compilation, latexmk, splitting input, CLI options | `references/compilation.md` | \input, \include, \includeonly, engines, options |

Only read the reference file(s) that match the task. Do not read all of them.

## Minimal Template

Use this unless the user provides their own preamble or a journal template. For other classes (book, report, beamer, letter), see `references/templates.md`.

```latex
\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[english]{babel}
\usepackage{amsmath, amssymb}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{geometry}
\geometry{margin=1in}

\title{[Title]}
\author{[Author]}
\date{\today}

\begin{document}
\maketitle

\begin{abstract}
[Abstract text]
\end{abstract}

\section{Introduction}
[Content]

\section{Methods}
[Content]

\section{Results}
[Content]

\section{Discussion}
[Content]

\bibliographystyle{plain}
\bibliography{references}

\end{document}
```

## Common Tasks

### Adding a figure

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{figures/result.png}
  \caption{Descriptive caption for the figure.}
  \label{fig:result}
\end{figure}
```

Reference in text with `\ref{fig:result}`. For more graphics options, see `references/graphics-color.md`.

### Adding a table

```latex
\begin{table}[htbp]
  \centering
  \begin{tabular}{lcc}
    \hline
    Method & Accuracy (\%) & F1 Score \\
    \hline
    Baseline & 85.2 & 0.83 \\
    Proposed & 91.7 & 0.90 \\
    \hline
  \end{tabular}
  \caption{Comparison of methods.}
  \label{tab:comparison}
\end{table}
```

For more tabular and environment options, see `references/environments.md`.

### Adding an equation

```latex
\begin{equation}
  \label{eq:loss}
  \mathcal{L} = -\sum_{i} y_i \log(\hat{y}_i)
\end{equation}
```

For math symbols, matrices, align environments, see `references/math.md`.

### Citing references

```latex
As shown in previous work~\cite{author2023title}, the method...
```

## Managing Citations

1. Create a `.bib` file with entries in BibTeX format
2. Use `\cite{key}` in the text
3. Include `\bibliographystyle{...}` and `\bibliography{...}` in the document
4. Compile with: `pdflatex → bibtex → pdflatex → pdflatex` (or use `latexmk`)

## Compilation

```bash
# Using latexmk (recommended)
latexmk -pdf document.tex

# Using pdflatex directly
pdflatex document.tex
bibtex document
pdflatex document.tex
pdflatex document.tex

# Using xelatex (for Unicode/OpenType fonts)
xelatex document.tex
```

For engine options, CLI flags, and splitting input, see `references/compilation.md`.

## Troubleshooting

| Error | Likely cause | Fix |
|-------|-------------|-----|
| `! Undefined control sequence` | Missing package | Add `\usepackage{...}` |
| `! File '...' not found` | Missing file or path | Check path is relative to the `.tex` file |
| `! LaTeX Error: Unknown float option 'H'` | Missing float package | Add `\usepackage{float}` |
| `! Missing $ inserted` | Math mode not closed | Check for missing `$` or `\]` |
| `! BibTeX: I couldn't open database file` | Wrong `.bib` path | Check `\bibliography{...}` path |
| Overfull `\hbox` | Text too wide for page | Reword or use `\sloppy` temporarily |
| Underfull `\vbox` | Page break issue | Usually cosmetic; ignore or adjust section break |

## Conversion from Markdown

To convert a markdown manuscript to LaTeX:

1. Use `pandoc` if available: `pandoc manuscript.md -o manuscript.tex`
2. If `pandoc` is not available, convert manually:
   - `#` headings → `\section{}`
   - `##` headings → `\subsection{}`
   - `###` headings → `\subsubsection{}`
   - `**bold**` → `\textbf{}`
   - `*italic*` → `\emph{}`
   - `![caption](path)` → `\includegraphics` in a `figure` environment
   - Tables: convert to `tabular` environment
   - Math: `$...$` and `$$...$$` are already valid LaTeX
   - Citations `[Author, Year]` → `\cite{key}` with a `.bib` entry