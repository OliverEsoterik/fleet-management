# LaTeX Layout Reference

Source: `latex2e.pdf` §5 Layout (pp38-47)

## Page Layout Commands

```latex
\onecolumn              % Switch to single-column (default for most classes)
\twocolumn              % Switch to two-column layout
\flushbottom            % Force all pages to same height
\raggedbottom           % Allow pages to have different heights
```

## Page Geometry

The `geometry` package is the standard way to set margins:

```latex
\usepackage{geometry}
\geometry{
  margin=1in,
  top=1in,
  bottom=1in,
  left=1.5in,           % wider left for binding
  right=1in,
  headheight=12pt,
  headsep=20pt,
  includehead,          % include header in specified area
  includefoot
}
```

Common shortcuts:
```latex
\geometry{margin=1in}
\geometry{hmargin=2cm, vmargin=3cm}
\geometry{left=2cm, right=2cm, top=2.5cm, bottom=2.5cm}
```

## Page Layout Parameters

Low-level length commands (set with `\setlength`):

```latex
\setlength{\textwidth}{16cm}       % Width of text body
\setlength{\textheight}{24cm}      % Height of text body
\setlength{\oddsidemargin}{0pt}    % Left margin for odd pages
\setlength{\evensidemargin}{0pt}   % Left margin for even pages (twoside)
\setlength{\topmargin}{0pt}
\setlength{\headheight}{12pt}
\setlength{\headsep}{25pt}
\setlength{\footskip}{30pt}        % Distance from text to footer
\setlength{\marginparwidth}{1.5cm} % Width of marginal notes
\setlength{\marginparsep}{5pt}     % Gap between text and margin note
```

## Column Layout

```latex
\twocolumn
\twocolumn[ \section{Title} ]     % Section spans both columns
\onecolumn
```

## Vertical Spacing

```latex
\vspace{10pt}                  % Flexible vertical space
\vspace*{10pt}                 % Vspace even at page start
\smallskip                     % ~3pt
\medskip                       % ~6pt
\bigskip                       % ~12pt
\vfill                         % Fill remaining vertical space
```