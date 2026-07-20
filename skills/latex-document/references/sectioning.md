# LaTeX Sectioning Reference

Source: `latex2e.pdf` §6 Sectioning (pp48-59)

## Sectioning Commands

Hierarchy from highest to lowest:

| Command | Level | Available in |
|---------|-------|-------------|
| `\part{title}` | -1 | all |
| `\chapter{title}` | 0 | report, book |
| `\section{title}` | 1 | all |
| `\subsection{title}` | 2 | all |
| `\subsubsection{title}` | 3 | all |
| `\paragraph{title}` | 4 | all |
| `\subparagraph{title}` | 5 | all |

## Usage

```latex
\section{Introduction}
\subsection{Motivation}
\subsubsection{Previous Work}
```

All sectioning commands share the same form:

```latex
\section{title}                    % numbered
\section*{title}                   % unnumbered (no number, no TOC entry)
\section[short]{long}              % short title in TOC/header
```

## Table of Contents

```latex
\tableofcontents
```

By default, `\tableofcontents` includes down to `\subsection`. Control depth:

```latex
\setcounter{tocdepth}{2}          % includes sections and subsections (default)
\setcounter{tocdepth}{3}          % also includes subsubsections
```

## Section Numbering

```latex
\setcounter{secnumdepth}{2}       % number down to subsections (default)
\setcounter{secnumdepth}{3}       % also number subsubsections
```

## Appendix

```latex
\appendix
\section{Data Tables}             % becomes A, B, C...
\section{Additional Results}
```

In book/report class:

```latex
\appendix
\chapter{Source Code}             % becomes Appendix A
```

## Cross-References

```latex
\section{Methods}
\label{sec:methods}

As shown in Section~\ref{sec:methods} on page~\pageref{sec:methods}.
```

The `~` produces a non-breaking space between the word and the reference.

## Customizing

```latex
\renewcommand{\thesection}{\Roman{section}}  % I, II, III instead of 1, 2, 3
\renewcommand{\thesubsection}{\thesection.\alph{subsection}}  % 1.a, 1.b
```