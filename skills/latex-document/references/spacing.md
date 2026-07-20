# LaTeX Spacing, Line Breaking, Page Breaking, Footnotes, and Lengths Reference

Source: `latex2e.pdf` §9 Line breaking (pp111-115), §10 Page breaking (pp116-118), §11 Footnotes (pp119-123), §14 Lengths (pp149-155), §19 Spaces (pp196-208)

## Line Breaking

```latex
\\              % line break (newline, not new paragraph)
\\[10pt]        % line break with extra vertical space
\newline        % same as \\
\linebreak      % allow line break here (with stretch)
\nolinebreak    % discourage line break
\hyphenation{hy-phen-a-tion}  % specify hyphenation for a word
\-              % optional hyphenation point
```

## Page Breaking

```latex
\newpage                    % force new page
\pagebreak                  % allow page break
\nopagebreak                % discourage page break
\pagebreak[4]               % with priority 0-4 (4 = force)
\clearpage                  % new page, flush all floats
\cleardoublepage            % new page, start on odd (right) page
```

## Footnotes

```latex
\footnote{Text of the footnote.}                     % basic footnote
\footnote[42]{Footnote with custom number.}          % custom number
\footnotemark                                         % placeholder for the mark
\footnotetext{Text for the preceding mark.}           % corresponding text
```

`\footnotemark` and `\footnotetext` are useful inside tables, minipages, or environments where `\footnote` doesn't work well.

Control parameters:

```latex
\setlength{\footnotesep}{7pt}    % space between footnotes
\setlength{\skip\footins}{10pt}  % space between text and footnotes
```

## Spaces

### Horizontal spaces

```latex
\enskip             % 0.5 em
\quad               % 1 em
\qquad              % 2 em
\enspace            % 0.5 em
\hspace{1cm}        % custom horizontal space
\hspace*{1cm}       % same, even at line start
\hfill              % stretch to fill line
\phantom{text}      % space equal to width of "text"
\,
\:                  % medium space (math mode)
\;                  % thick space (math mode)
\␣                  % backslash + space = interword space
~                   % non-breaking space
\@.                 % period ends sentence (extra space after)
```

### Vertical spaces

```latex
\vspace{10pt}        % vertical space
\vspace*{10pt}       % vertical space, even at page start
\smallskip           % ~3pt
\medskip             % ~6pt
\bigskip             % ~12pt
\vfill               % fill remaining vertical space
```

## Lengths

### Defining and using lengths

```latex
\newlength{\mylen}                % define a new length
\setlength{\mylen}{10pt}          % set its value
\setlength{\mylen}{2cm}           % any valid unit
\addtolength{\mylen}{5pt}         % add to a length
\settowidth{\mylen}{Some text}    % set to width of text
\settoheight{\mylen}{Some text}   % set to height of text
\settodepth{\mylen}{Some text}    % set to depth of text
\the\mylen                        % print the length value
```

### Valid units

| Unit | Value |
|------|-------|
| `pt` | point (1/72.27 in) |
| `mm` | millimeter |
| `cm` | centimeter |
| `in` | inch |
| `ex` | height of 'x' in current font |
| `em` | width of 'M' in current font |
| `\textwidth` | width of text area |
| `\textheight` | height of text area |
| `\linewidth` | width of current line |
| `\columnwidth` | width of current column |
| `\paperwidth` | paper width |
| `\paperheight` | paper height |

### Stretchable lengths (glue)

```latex
\setlength{\parskip}{0pt plus 1pt}       % stretchable
\setlength{\parskip}{0pt plus 1pt minus 1pt}  % stretchable and shrinkable
\fill                                      % infinite stretch
\setlength{\parskip}{0pt plus 1fill}       % stronger than \hfill
```