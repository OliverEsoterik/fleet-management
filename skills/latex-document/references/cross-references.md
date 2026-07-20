# LaTeX Cross-Reference Reference

Source: `latex2e.pdf` §7 Cross references (pp60-63)

## Basic Cross-References

```latex
\label{key}          % mark a location
\ref{key}            % print the number (section, equation, figure, etc.)
\pageref{key}        % print the page number
```

## Label Placement

Labels must come **after** the thing they reference:

```latex
\section{Introduction}
\label{sec:intro}

\begin{equation}
  E = mc^2
  \label{eq:einstein}
\end{equation}

\begin{figure}
  \centering
  \includegraphics{plot.png}
  \caption{Results}
  \label{fig:results}
\end{figure}
```

## Referencing

```latex
As shown in Section~\ref{sec:intro}, equation~\ref{eq:einstein}, and
Figure~\ref{fig:results} on page~\pageref{fig:results}.
```

The `~` prevents a line break between the word and the number.

## Named References

With the `hyperref` package, references become clickable links:

```latex
\usepackage[colorlinks=true, linkcolor=blue, citecolor=blue, urlcolor=blue]{hyperref}
```

## Common Label Naming Conventions

| Prefix | For |
|--------|-----|
| `sec:` | sections |
| `fig:` | figures |
| `tab:` | tables |
| `eq:` | equations |
| `ch:` | chapters |
| `lst:` | listings |
| `alg:` | algorithms |
| `app:` | appendix |

## Advanced: `\ref` Variants

With `hyperref`:

```latex
\autoref{sec:intro}   % prints "Section 1" instead of just "1"
\nameref{sec:intro}   % prints the section title
```

With `cleveref` package:

```latex
\usepackage{cleveref}
\Cref{fig:results,tab:data}  % prints "Figures 1 and 2"
```

## Two-Pass Compilation

Cross-references require two compilation passes. Use `latexmk`:

```bash
latexmk -pdf document.tex
```

Or manually:

```bash
pdflatex document.tex
pdflatex document.tex
```