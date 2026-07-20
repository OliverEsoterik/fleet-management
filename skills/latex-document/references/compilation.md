# LaTeX Compilation Reference

Source: `latex2e.pdf` §24 Splitting the input (pp241-244), §27 Input/output (pp264-270), §28 Command line interface (pp271-275)

## Compilation Engines

| Command | Engine | Output |
|---------|--------|--------|
| `pdflatex` | pdfTeX | PDF |
| `xelatex` | XeTeX | PDF (Unicode, OpenType/TrueType fonts) |
| `lualatex` | LuaTeX | PDF (Unicode, fontspec, Lua scripting) |
| `latex` | TeX | DVI (convert to PDF with `dvipdfmx`) |

## Using latexmk (Recommended)

```bash
latexmk -pdf document.tex                    # pdflatex
latexmk -xelatex document.tex                # xelatex
latexmk -lualatex document.tex               # lualatex
latexmk -pdf -pvc document.tex               # continuous preview mode
latexmk -c                                    # clean auxiliary files
latexmk -C                                    # clean everything (including PDF)
```

## Manual Compilation

```bash
# Simple document (no citations)
pdflatex document.tex
pdflatex document.tex            # resolve cross-references

# With BibTeX citations
pdflatex document.tex
bibtex document
pdflatex document.tex
pdflatex document.tex

# With makeindex
pdflatex document.tex
makeindex document
pdflatex document.tex
```

## Command Line Options

```bash
# Common pdflatex options
pdflatex -interaction=nonstopmode document.tex    # don't stop on errors
pdflatex -interaction=batchmode document.tex      # even quieter
pdflatex -jobname=final document.tex              # output as final.pdf
pdflatex -output-directory=build document.tex     # output in build/
pdflatex -shell-escape document.tex               # allow shell commands
pdflatex -synctex=1 document.tex                  # SyncTeX (editor sync)
pdflatex -halt-on-error document.tex              # stop at first error
```

## Splitting Input Files

### `\input` — include file (no new page)

```latex
\input{introduction}          % includes introduction.tex
\input{chapters/intro}        % relative path
```

### `\include` — include with page break

```latex
\include{chapter1}            % inserts \clearpage before and after
\include{chapter2}
```

### `\includeonly` — select which files to include

```latex
\includeonly{chapter1,chapter3}   % only compile these
\include{chapter1}                  % others are skipped
\include{chapter2}                  % (skipped)
\include{chapter3}
```

### Prefer `\input` for sections

Use `\input` for sections within a chapter, `\include` for whole chapters:

```latex
\chapter{Introduction}
\input{sections/background}
\input{sections/motivation}
```

## Front/Back Matter (book class)

```latex
\frontmatter        % Roman page numbers, unnumbered chapters
\mainmatter         % Arabic page numbers
\backmatter         % Unnumbered chapters (bibliography, index)
```

## TOC and Lists

```latex
\tableofcontents
\listoffigures
\listoftables
```

Customize TOC depth:

```latex
\setcounter{tocdepth}{2}        % sections and subsections
```

## Auxiliary Files

| Extension | Purpose |
|-----------|---------|
| `.aux` | Cross-references, citations |
| `.bbl` | Bibliography (output from bibtex) |
| `.blg` | BibTeX log |
| `.idx` | Raw index entries |
| `.ind` | Processed index |
| `.ilg` | Index log |
| `.lof` | List of figures |
| `.lot` | List of tables |
| `.log` | Compilation log |
| `.out` | Hyperref bookmarks |
| `.synctex.gz` | Editor synchronization |
| `.toc` | Table of contents |
| `.fls` | File list (with `-recorder`) |
| `.xdv` | XeTeX intermediate DVI |