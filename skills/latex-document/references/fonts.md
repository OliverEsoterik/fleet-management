# LaTeX Font Reference

Source: `latex2e.pdf` §4 Fonts (pp26-37)

## Font Families

LATEX's New Font Selection Scheme (NFSS) provides three main families:

| Command | Shape | Example |
|---------|-------|---------|
| `\textrm{...}` | Roman (serif) | default |
| `\textsf{...}` | Sans-serif | |
| `\texttt{...}` | Typewriter (mono) | |

## Font Styles

```latex
\textit{italic}
\textbf{bold}
\textsl{slanted}
\textsc{small caps}
\emph{emphasized}         % usually italic, toggles contextually
\textnormal{normal}       % reset to document font
```

## Font Sizes

```latex
\tiny
\scriptsize
\footnotesize
\small
\normalsize              % default
\large
\Large
\LARGE
\huge
\Huge
```

These are declarations, not commands with arguments. They apply to everything after them until the group ends:

```latex
{\Large This is large text.} Back to normal.
```

## Font Encoding

```latex
\usepackage[T1]{fontenc}    % Cork encoding — 256 glyphs, proper hyphenation
\usepackage[utf8]{inputenc} % Input encoding (default since 2018)
```

T1 is the encoding for European languages. Without it, accented characters may not hyphenate correctly.

## Common Font Packages

| Package | Effect |
|---------|--------|
| `\usepackage{lmodern}` | Latin Modern (default, extended) |
| `\usepackage{mathptmx}` | Times-like (text + math) |
| `\usepackage{helvet}` | Helvetica (sans-serif) |
| `\usepackage{courier}` | Courier (typewriter) |
| `\usepackage{mathpazo}` | Palatino (text + math) |

## XeTeX / LuaTeX Fonts

With XeLaTeX or LuaLaTeX, use system fonts directly:

```latex
\usepackage{fontspec}
\setmainfont{TeX Gyre Termes}
\setsansfont{TeX Gyre Heros}
\setmonofont{TeX Gyre Cursor}
```

## Math Mode Fonts

```latex
\mathrm{...}    % Roman
\mathit{...}    % Italic
\mathbf{...}    % Bold
\mathsf{...}    % Sans-serif
\mathtt{...}    % Typewriter
\mathcal{...}   % Calligraphic
\mathbb{...}    % Blackboard bold (requires amsfonts or amssymb)
\mathfrak{...}  % Fraktur (requires amsfonts or amssymb)
```