# LaTeX Templates Reference

Source: `latex2e.pdf` §3 Document classes (pp22-25), Appendix A (pp276+)

## Document Class Options

```
\documentclass[options]{class}
```

**Common classes:**

| Class | Purpose |
|-------|---------|
| `article` | Short documents, papers, no chapters |
| `report` | Longer documents with chapters |
| `book` | Books with front/back matter, chapters |
| `beamer` | Presentations |
| `letter` | Letters |

**Common options:** `10pt`, `11pt`, `12pt`, `a4paper`, `letterpaper`, `twocolumn`, `twoside`, `draft`, `landscape`

## Article Template

```latex
\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[english]{babel}
\usepackage{amsmath, amssymb}
\usepackage{graphicx}
\usepackage[colorlinks=true]{hyperref}
\usepackage{geometry}
\geometry{margin=1in}

\title{Title}
\author{Author}
\date{\today}

\begin{document}
\maketitle

\begin{abstract}
...
\end{abstract}

\section{Introduction}
\label{sec:intro}

\section{Methods}
\label{sec:methods}

\section{Results}
\label{sec:results}

\section{Discussion}
\label{sec:discussion}

\bibliographystyle{plain}
\bibliography{references}
\end{document}
```

## Report Template

```latex
\documentclass[11pt,a4paper]{report}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{amsmath, amssymb}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{geometry}
\geometry{margin=1in}

\title{Title}
\author{Author}
\date{\today}

\begin{document}
\maketitle
\tableofcontents

\chapter{Introduction}
\label{ch:intro}

\chapter{Methods}
\label{ch:methods}

\chapter{Results}
\label{ch:results}

\chapter{Conclusion}
\label{ch:conclusion}

\bibliographystyle{plain}
\bibliography{references}
\end{document}
```

## Book Template

```latex
\documentclass[11pt,a4paper,twoside]{book}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{amsmath, amssymb}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{geometry}
\geometry{margin=1in}

\title{Title}
\author{Author}
\date{\today}

\begin{document}
\frontmatter
\maketitle
\tableofcontents

\mainmatter
\chapter{Introduction}
\label{ch:intro}

\chapter{Main Topic}
\label{ch:main}

\appendix
\chapter{Data Tables}

\backmatter
\bibliographystyle{plain}
\bibliography{references}
\end{document}
```

## Beamer Template

```latex
\documentclass{beamer}
\usetheme{default}  % Options: default, Berlin, Madrid, Copenhagen, Warsaw, etc.
\usepackage[utf8]{inputenc}
\usepackage{amsmath, amssymb}
\usepackage{graphicx}

\title{Title}
\author{Author}
\date{\today}

\begin{document}
\frame{\titlepage}

\begin{frame}{Outline}
\tableofcontents
\end{frame}

\section{Introduction}
\begin{frame}{Slide Title}
\begin{itemize}
  \item First bullet
  \item Second bullet
\end{itemize}
\end{frame}

\section{Main Content}
\begin{frame}{With Columns}
\begin{columns}
  \column{0.5\textwidth}
  Left column content
  \column{0.5\textwidth}
  Right column content
\end{columns}
\end{frame}
\end{document}
```

## Letter Template

```latex
\documentclass{letter}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

\address{Sender\\123 Street\\City}
\signature{Sender Name}

\begin{document}
\begin{letter}{Recipient\\456 Avenue\\City}

\opening{Dear Recipient,}

Letter body text.

\closing{Sincerely,}

\end{letter}
\end{document}
```