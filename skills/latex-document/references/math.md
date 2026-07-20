# LaTeX Math Reference

Source: `latex2e.pdf` §16 Math formulas (pp160-188)

## Inline vs Display Math

```latex
Inline: $E = mc^2$ or \( E = mc^2 \)
Display: \[ E = mc^2 \] or \begin{equation} ... \end{equation}
```

## Common Math Symbols

### Greek letters

```latex
\alpha \beta \gamma \delta \epsilon \varepsilon
\zeta \eta \theta \vartheta \iota \kappa \lambda \mu \nu
\xi \pi \varpi \rho \varrho \sigma \varsigma \tau
\upsilon \phi \varphi \chi \psi \omega

\Gamma \Delta \Theta \Lambda \Xi \Pi \Sigma \Upsilon \Phi \Psi \Omega
```

### Operators

```latex
+ - \times \div \pm \mp \cdot \circ
\cup \cap \setminus \subset \supset \subseteq \supseteq
\in \notin \ni \forall \exists \emptyset \varnothing
\wedge \vee \oplus \otimes \odot
```

### Relations

```latex
= \neq \approx \equiv \sim \simeq \cong \propto
< > \leq \geq \ll \gg \prec \succ \preceq \succeq
\perp \parallel \mid \models \dashv \vdash
```

### Arrows

```latex
\to \rightarrow \leftarrow \Rightarrow \Leftarrow
\mapsto \longrightarrow \longleftarrow \Longrightarrow
\uparrow \downarrow \leftrightarrow \Leftrightarrow
\nearrow \searrow \nwarrow \swarrow
```

### Dots

```latex
\dots \cdots \vdots \ddots
```

### Delimiters

```latex
( ) [ ] \{ \} \langle \rangle \lfloor \rfloor \lceil \rceil
\| \|                     % double vertical bars
\left( ... \right)         % auto-sized delimiters
\bigl( \bigr) \biggl( \biggr) \Bigl( \Bigr)  % manual sizing
```

## Fractions, Roots, and Integrals

```latex
\frac{a}{b}                    % fraction
\sqrt{x}                       % square root
\sqrt[n]{x}                    % nth root
\int_a^b f(x)\,dx              % integral
\iint \iiint \oint             % multiple integrals
\sum_{i=1}^n                   % sum
\prod_{i=1}^n                  % product
\lim_{x \to \infty}            % limit
```

## Accents in Math

```latex
\hat{a} \check{a} \tilde{a} \acute{a} \grave{a}
\dot{a} \ddot{a} \breve{a} \bar{a} \vec{a}
\widehat{ABC} \widetilde{ABC}
```

## Functions and Named Operators

```latex
\sin \cos \tan \log \ln \exp \det \dim \hom \ker
\lim \max \min \sup \inf \arg \deg \gcd \Pr
```

## Matrices

```latex
\begin{matrix}
  a & b \\
  c & d
\end{matrix}

\begin{pmatrix}   % with parentheses
  a & b \\
  c & d
\end{pmatrix}

\begin{bmatrix}   % with brackets
  a & b \\
  c & d
\end{bmatrix}

\begin{cases}     % piecewise
  x & \text{if } y > 0 \\
  0 & \text{otherwise}
\end{cases}
```

## Multi-line Equations

```latex
\begin{align}
  x &= y + z \\
  y &= a + b + c
\end{align}

\begin{align*}
  x &= y + z \\
  y &= a + b + c    % unnumbered
\end{align}

\begin{alignat}{2}
  x &= y \quad & a &= b \\
  z &= w \quad & c &= d
\end{alignat}

\begin{gather}
  a = b + c \\
  d = e + f
\end{gather}
```

## Text in Math

```latex
\text{plain text}       % requires amsmath
\mathrm{ROMAN}          % roman font
\mathbf{bold}           % bold
\mathit{italic}         % italic (math)
\mathbb{BB}             % blackboard bold (amsfonts)
```

## Spacing in Math

```latex
\,       % thin space (3/18 em)
\:       % medium space (4/18 em)
\;       % thick space (5/18 em)
\!       % negative thin space
\quad    % 1 em
\qquad   % 2 em
```

## Common Packages

| Package | Provides |
|---------|----------|
| `amsmath` | `align`, `gather`, `cases`, `\text`, `\overset`, `\underset`, `\xrightarrow` |
| `amssymb` | `\mathbb`, `\therefore`, `\because`, `\varnothing`, `\triangleq` |
| `amsfonts` | `\mathfrak`, `\mathcal` (calligraphic), `\mathbb` |
| `mathtools` | Extensions of amsmath — `\coloneqq`, `\DeclarePairedDelimiter` |