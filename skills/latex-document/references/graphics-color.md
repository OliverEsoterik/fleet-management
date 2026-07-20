# LaTeX Graphics, Color, and Boxes Reference

Source: `latex2e.pdf` §20 Boxes (pp209-215), §21 Graphics (pp216-226), §22 Color (pp227-230)

## Graphics

### Including graphics

```latex
\usepackage{graphicx}     % standard package

\includegraphics{file.png}                           % original size
\includegraphics[width=0.8\textwidth]{file.png}      % scale to width
\includegraphics[height=5cm]{file.png}               % scale to height
\includegraphics[width=0.5\textwidth, keepaspectratio]{file.png}
\includegraphics[scale=0.5]{file.png}                % scale factor
\includegraphics[angle=45, width=3cm]{file.png}      % rotated + scaled
```

### Supported formats

| Engine | Supported formats |
|--------|------------------|
| pdflatex | PDF, PNG, JPEG |
| xelatex | PDF, PNG, JPEG, EPS |
| lualatex | PDF, PNG, JPEG, EPS |
| latex (dvi) | EPS |

### Graphics path

```latex
\usepackage{graphicx}
\graphicspath{{figures/}{images/}}    % search these directories
```

### Clipping and trimming

```latex
\includegraphics[trim=1cm 2cm 1cm 2cm, clip, width=5cm]{file.png}
% trim: left bottom right top (all at once)
```

## Color

### Using colors

```latex
\usepackage{color}         % or \usepackage{xcolor} — more features

\textcolor{red}{red text}
\colorbox{yellow}{text with yellow background}
\fcolorbox{red}{yellow}{red border, yellow fill}
```

### Named colors

Basic: `red`, `green`, `blue`, `cyan`, `magenta`, `yellow`, `black`, `gray`, `white`, `darkgray`, `lightgray`, `brown`, `lime`, `olive`, `orange`, `pink`, `purple`, `teal`, `violet`

### Defining colors

```latex
\definecolor{mycolor}{rgb}{0.2, 0.5, 0.8}       % RGB (0.0-1.0)
\definecolor{mycolor}{cmyk}{0.5, 0.2, 0.0, 0.1} % CMYK
\definecolor{mycolor}{gray}{0.5}                  % Gray 0.0-1.0
\definecolor{mycolor}{HTML}{336699}               % Hex HTML
```

### Color in boxes

```latex
\colorbox{red}{\textcolor{white}{Text}}          % white on red
\fcolorbox{blue}{yellow}{Text}                   % blue border, yellow fill
\colorbox{blue!20}{Text}                         % 20% blue (xcolor)
```

## Boxes

### Simple boxes

```latex
\mbox{non-breaking box}                    % unbreakable box
\makebox[width][position]{text}            % box of explicit width
\makebox[2cm][r]{right-aligned}            % alignment: l, r, c, s
\fbox{bordered box}                        % box with frame
\framebox[width][position]{text}           % framed box with width
\raisebox{lift}[height][depth]{text}       % raise/lower text
```

### Paragraph boxes

```latex
\parbox[position][height][inner-pos]{width}{text}
\parbox[t]{5cm}{...}                      % top-aligned, 5cm wide
\parbox[b]{0.5\textwidth}{...}            % bottom-aligned
```

### Save boxes (for reuse)

```latex
\newsavebox{\mybox}                        % declare
\sbox{\mybox}{content}                     % save
\savebox{\mybox}[width][pos]{content}      % save with options
\usebox{\mybox}                            % use
```

### Rule (horizontal line)

```latex
\rule[raise]{width}{height}
\rule{3cm}{0.4pt}                         % thin horizontal line
\rule{0.4pt}{3cm}                         % thin vertical line
\rule[-2pt]{5cm}{1pt}                     % raised down 2pt
```