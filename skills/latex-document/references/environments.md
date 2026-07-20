# LaTeX Environments Reference

Source: `latex2e.pdf` §8 Environments (pp64-110)

## List Environments

### `itemize` — bulleted list

```latex
\begin{itemize}
  \item First item
  \item Second item
    \begin{itemize}
      \item Nested item
    \end{itemize}
\end{itemize}
```

### `enumerate` — numbered list

```latex
\begin{enumerate}
  \item Step one
  \item Step two
    \begin{enumerate}
      \item Sub-step
    \end{enumerate}
\end{enumerate}
```

### `description` — labelled list

```latex
\begin{description}
  \item[Term] Definition text.
  \item[Another term] Longer definition here.
\end{description}
```

## Text Environments

### `quote` — short quotation

```latex
\begin{quote}
  A short quotation, indented on both sides.
\end{quote}
```

### `quotation` — longer quotation (paragraphs indented)

```latex
\begin{quotation}
  A longer quotation. Paragraphs are indented.

  Second paragraph of the quotation.
\end{quotation}
```

### `verse` — poetry

```latex
\begin{verse}
  There once was a man from Nantucket \\
  Who kept all his cash in a bucket.
\end{verse}
```

### `verbatim` — literal text (no interpretation)

```latex
\begin{verbatim}
  #include <stdio.h>
  int main() { return 0; }
\end{verbatim}
```

Inline: `\verb|code|` (any delimiter works, not just `|`).

### `center` — centered text

```latex
\begin{center}
  Centered line \\
  Another centered line
\end{center}
```

### `flushleft` / `flushright`

```latex
\begin{flushleft}
  Left-aligned text.
\end{flushleft}

\begin{flushright}
  Right-aligned text.
\end{flushright}
```

## Box and Layout Environments

### `minipage` — box of text with full formatting

```latex
\begin{minipage}[position]{width}
  Content with its own paragraph formatting,
  footnotes, etc.
\end{minipage}
```

Position: `t` (top), `b` (bottom), `c` (center — default).

Useful for side-by-side content:

```latex
\begin{minipage}[t]{0.48\textwidth}
  Left column content.
\end{minipage}
\hfill
\begin{minipage}[t]{0.48\textwidth}
  Right column content.
\end{minipage}
```

### `abstract` — article abstract

```latex
\begin{abstract}
  Summary of the paper.
\end{abstract}
```

## Tabular Environments

### `tabular` — table with alignment

```latex
\begin{tabular}{l|c|r}
  \hline
  Left & Center & Right \\
  \hline
  Data 1 & Data 2 & Data 3 \\
  \hline
\end{tabular}
```

Column specifiers: `l` (left), `c` (center), `r` (right), `p{width}` (paragraph), `|` (vertical rule).

### `tabbing` — tab stops (like typewriter tabs)

```latex
\begin{tabbing}
  Name \= Age \= City \\
  Alice \> 30 \> London \\
  Bob   \> 25 \> Paris
\end{tabbing}
```

## Math Environments

### Inline math

```latex
$E = mc^2$         % or \( E = mc^2 \)
```

### Display math

```latex
\[ E = mc^2 \]     % unnumbered

\begin{equation}
  E = mc^2
  \label{eq:energy}
\end{equation}

\begin{align}
  x &= y + z \\
  y &= a + b
  \label{eq:y}
\end{align}

\begin{equation*}
  \text{Unnumbered equation}
\end{equation*}
```

### `array` — math arrays

```latex
\[
  \begin{array}{lcr}
    a & b & c \\
    d & e & f
  \end{array}
\]
```

## Float Environments

### `figure` — floating illustration

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{file.png}
  \caption{Figure caption.}
  \label{fig:label}
\end{figure}
```

Placement specifiers: `h` (here), `t` (top), `b` (bottom), `p` (float page), `!` (override restrictions). Default: `tbp`.

### `table` — floating table

```latex
\begin{table}[htbp]
  \centering
  \begin{tabular}{lcc}
    \hline
    A & B & C \\
    \hline
  \end{tabular}
  \caption{Table caption.}
  \label{tab:label}
\end{table}
```

## The `picture` Environment

Simple line drawings using LATEX primitives:

```latex
\begin{picture}(width,height)(x0,y0)
  \put(x,y){\line(x_slope,y_slope){length}}
  \put(x,y){\circle{diameter}}
  \put(x,y){\framebox(width,height){text}}
\end{picture}
```

For complex drawings, use `tikz` or `pgf` packages instead.