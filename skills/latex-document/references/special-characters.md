# LaTeX Special Characters and Accents Reference

Source: `latex2e.pdf` §23 Special insertions (pp231-240)

## Reserved Characters

These characters have special meaning in LaTeX and must be escaped:

| Character | How to print | Note |
|-----------|-------------|------|
| `\` | `\textbackslash` | Backslash |
| `{` | `\{` | Opening brace |
| `}` | `\}` | Closing brace |
| `%` | `\%` | Comment character |
| `$` | `\$` | Math mode |
| `&` | `\&` | Tabular column separator |
| `#` | `\#` | Parameter |
| `^` | `\^{}` | Superscript (in math) |
| `_` | `\_` | Subscript (in math) |
| `~` | `\textasciitilde` | Non-breaking space |

## Accents

```latex
\'{o}   ó    acute accent
\`{o}   ò    grave accent
\"{o}   ö    umlaut / diaeresis
\^{o}   ô    circumflex
\~{o}   õ    tilde
\={o}   ō    macron
\.{o}   ȯ    dot accent
\u{o}   ŏ    breve
\v{o}   ǒ    caron / háček
\H{o}   ő    long Hungarian umlaut
\t{oo}        tie-after accent
\c{c}   ç    cedilla
\d{o}         dot-under
\b{o}         bar-under
\r{a}   å    ring
```

## Non-English Characters

```latex
\oe \OE     œ Œ    ligature OE
\ae \AE     æ Æ    ligature AE
\aa \AA     å Å    ring a
\o \O       ø Ø    slashed o
\l \L       ł Ł    slashed l
\ss \SS     ß      sharp s (eszett)
"`          „      German low double quote (requires ngerman)
"'          "      German high double quote (requires ngerman)
```

## Text Symbols

```latex
\dots         …        ellipsis
\ldots        …        ellipsis (lower)
\textdagger   †        dagger
\textdaggerdbl ‡       double dagger
\textbullet   •        bullet
\textcopyright ©       copyright
\textregistered ®      registered
\texttrademark ™       trademark
\S            §        section sign
\P            ¶        pilcrow
\textasteriskcentered *   centered asterisk
\textbackslash \       backslash
\textbar       |       vertical bar
\textless      <       less-than
\textgreater   >       greater-than
\textasciitilde ~      tilde
\textasciicircum ^     circumflex
\$            $        dollar
\pounds        £       pound sterling
\texteuro      €       euro (requires textcomp or eurosym)
\textyen       ¥       yen
\dag           †       dagger
\ddag          ‡       double dagger
\copyright     ©       copyright
```

## Date and Time

```latex
\today        % current date (e.g., "July 20, 2025")
```

## Ligatures

LaTeX automatically handles these input sequences as ligatures:

```
ff → ff, fi → fi, fl → fl, ffi → ffi, ffl → ffl
```

Break a ligature with `\mbox{}` or `"`:

```latex
shelf{}ul    % prevents "ful" ligature
```

## Dashes and Hyphens

```latex
-        hyphen:   X-ray
--       en-dash:  pages 1--10
---      em-dash:  yes---or no
$-$      minus:    $x-y$
```

## Quotation Marks

```latex
`single quotes'          % backtick, apostrophe
``double quotes''        % two backticks, two apostrophes
``So she said''          % correct: "So she said"
```

For French-style:

```latex
\og guillemets\fg{}      % requires babel (french)
```