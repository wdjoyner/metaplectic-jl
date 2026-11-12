# Metaplectic Jacquet–Langlands Transfer

A research book toward a metaplectic Jacquet–Langlands transfer for
division algebras of prime degree.

This is ongoing mathematical research. The book distinguishes
complete proofs, results established in the literature or elsewhere
in the book, conditional statements, and open problems. **The full
metaplectic Jacquet–Langlands correspondence is not claimed to have
been established.**

## The book

The working document is `book/mjl_book_draft.tex` (*On a metaplectic
Jacquet–Langlands transfer for division algebras of prime degree*, by
David Joyner, Claude and ChatGPT; currently Draft 2), compiled to
`book/mjl_book_draft.pdf`. Build it with:

```bash
cd book
pdflatex mjl_book_draft.tex
pdflatex mjl_book_draft.tex   # second pass for cross-references
makeindex mjl_book_draft.idx  # builds the index
pdflatex mjl_book_draft.tex   # final pass to place the index
```

### Chapters

| Chapter | Contents |
|---------|----------|
| 1 | Introduction and overview, including the running example |
| 2 | Literature review |
| 3 | Background and notation |
| 4 | Local matching and a global transfer under elliptic-support conditions |
| 5 | Matching of arbitrary functions and an improved global transfer |
| 6 | The division-algebra side and its local character transform |
| 7 | Local power maps, toral positivity, and conditional global comparison |
| 8 | The rank-two wild place: toral positivity and the nonabelian gluing problem |
| 9 | Summary of results |
| 10 | Glossary |

Chapters 4–7 correspond to the series' former Parts I–IV, and Chapter
8 to the former standalone companion paper on the rank-two wild case.
The book's revision log is `book/mjl_book_revision_log_draftK.tex`,
where `K` is the draft number. The log of Draft 2 lists every addition
that still needs refereeing and gives a concordance of the numbers
that changed.

### The setting

- `K` is a totally imaginary number field containing the `n`th roots
  of unity, with `n` odd.
- `r` is a prime with `gcd(n, r) = 1`.
- `D` is a central division algebra of degree `r` over `K`, ramified
  at a finite set of places `S`.

The book compares two `n`-fold covering groups:

- the cover of `D^×` from the author's corrected 1988 paper on the
  metaplectic analog of Kazhdan's "endoscopic" lifting;
- the Kazhdan–Patterson cover of `GL(r)` with parameter `c_v`, where
  `n` divides `r − 1 + 2 r c_v`.

Both covers sit inside one ambient cover, constructed in Chapter 4.

### Running example

Every chapter tests its constructions on one concrete case, stated as
Example 1.3.1 in Chapter 1: `K = Q(ζ₃)`, `n = 3`, `r = 2`, and the
quaternion algebra `D = (−1, 4 − ζ₃)` over `K`. This algebra is
ramified exactly at the prime above 3 (the wild place, where
`b_D = 3` and `c_D = 27`) and at one prime above 7 (a tame place).
Chapter 1 also records, as Remark 1.3.2, that the example satisfies
the standing hypotheses drawn on from [JC26], [FK86] and [FK88]. Each
later chapter has its own short "running example" subsection
cross-referencing Example 1.3.1, and `notes/mjl_running_example.tex`
works the case out in detail across Chapters 4–8; it is cited in the
book as [JC26b].

The approach follows the classical trace-formula proof of the
Jacquet–Langlands correspondence. It uses the metaplectic correspondence
of Flicker–Kazhdan (Publ. Math. IHÉS 64, 1986), together with the
corrections of J. Zou (arXiv:2209.05852).

### Main open problems

- **Integrality of `L_D` at places dividing `n`.** It is open whether
  `L_D` maps irreducible characters to irreducible genuine characters
  there in general. For the running example (`r = 2`, `n = 3`,
  `F = Q_3(ζ_3)`) Chapter 8 settles the trivial character and all rows
  trivial on the third congruence subgroup; rows of higher level, and
  other `p` and `F`, remain open (see Chapter 8, §8.15, Future
  Directions).
- **The full comparison of `D^×` with its cover.** The comparison is
  proved only conditionally. What is missing is matching at the places
  where `D` splits and at the complex places.
- **Removing auxiliary hypotheses.** The support and packet hypotheses
  used in Chapters 4–5 should eventually be removed.

## Status labels

| Label | Meaning |
|-------|---------|
| **(P)** | Proved in the book |
| **(E)** | Established in the literature or elsewhere in the book |
| **(O)** | Proof outlined but not fully established |
| **(C)** | Conjectural, or conditional on stated unproved hypotheses |
| **(P^c)** | Proved modulo an exhaustive exact computation whose script is in the repository (Chapter 8 only) |

The full definitions and the book's notation are in Chapter 3
(Background and notation). The cocycle normalization is in Chapter 10
(Glossary).

## Repository layout

```
book/       The book: mjl_book_draft.tex / .pdf, chapters/,
            bibliography.tex, and the revision log
glossary.tex  Shared glossary of notation, conventions and status
            labels, input by each frozen Part below
notes/      Supporting notes, including the running example
software/   Supporting code (MIT License)
part-I/     Part I drafts (.tex, .pdf) and revision logs (frozen)
part-II/    Part II drafts and revision logs (frozen)
part-III/   Part III drafts and revision logs (frozen)
part-IV/    Part IV drafts, revision logs, referee reports, the
            rank-two toral positivity note, and the rank-two
            companion paper (frozen)
```

### Earlier standalone papers (frozen, superseded by the book)

Before being combined into the book, this research circulated as
four standalone papers (Parts I–IV) plus a companion paper on the
rank-two wild case. Those drafts remain in `part-I/` through
`part-IV/` for reference and are frozen at their last versions; all
further work happens in the book. Each part's full title began *"A
metaplectic Jacquet–Langlands transfer for division algebras of prime
degree."*

- **Part I → Chapter 4.** Construction of the covers, good elements,
  matching of regular-supported test functions, and a global
  transfer ("Theorem C") under a hypothesis `(Hyp_D)`.
- **Part II → Chapter 5.** Matching of arbitrary genuine test
  functions, and a strengthened global transfer ("Theorem C′") under
  a weaker hypothesis `(Hyp_D')`.
- **Part III → Chapter 6.** The unitary transform `L_D`, its
  bijectivity away from places dividing `n`, a divisibility test at
  places dividing `n`, and local-to-global results for `n`th powers.
- **Part IV → Chapter 7.** Cocycle reconciliation, the
  Flicker–Kazhdan good-element criterion, power-map kernels and
  indices, global good classes, and the toral positivity criterion at
  places dividing `n`.
- **Companion paper → Chapter 8.** The rank-two wild case: toral
  positivity and the nonabelian gluing problem, including the proof
  of Target A for the running example.

Parts I–III input the shared glossary `glossary.tex` from the
repository root, so they must be compiled from inside their folders:

```bash
cd part-I
pdflatex mjl_part1_draft11.tex
pdflatex mjl_part1_draft11.tex   # second pass for cross-references
cd ../part-II
pdflatex mjl_part2_draft10.tex
pdflatex mjl_part2_draft10.tex
cd ../part-III
pdflatex mjl_part3_draft10.tex
pdflatex mjl_part3_draft10.tex
```

Part IV (concluding Draft 6) is self-contained:

```bash
cd part-IV
pdflatex mjl_part4_draft6.tex
pdflatex mjl_part4_draft6.tex   # second pass for cross-references
```

## Software

- `software/toral_coefficient_check.py` is an independent check of
  the coefficient formulas behind the rank-two toral positivity
  results in Chapter 8.
- It runs over a range of residue characteristics, ramification
  indices and residue degrees, for both unramified and ramified
  quadratic extensions.
- For each case it verifies that every coefficient is a nonnegative
  integer, and that the total equals `|n|^(−1)`.

Run it with:

```bash
python3 software/toral_coefficient_check.py
```

## Review process

The book is written and refereed with AI assistance:

- ChatGPT (OpenAI) and Claude (Anthropic) have each drafted and
  refereed material in the book.
- Referee reports and responses to them are kept with the earlier
  standalone papers in `part-I/` through `part-IV/`.
- Each referee report states which sources were checked against
  originals, and which were not.

Independent human review is the next step. Comments, corrections and
referee reports are welcome through GitHub Issues.

## Licensing

- **Book and notes:** the book, its PDF, and original explanatory
  material are licensed under Creative Commons Attribution 4.0
  International (CC BY 4.0).
- **Software:** software in `software/` is licensed under the MIT
  License.
- **Third-party works:** these remain subject to their own licenses and
  are not relicensed by this repository. In particular, previously
  published articles by the author, and revised versions of them, are
  **not** included here, and nothing here relicenses them.

## Citation

When citing a result, identify the chapter and section, for example:
*Chapter 7, Theorem 7.5.2*. Theorem numbers can change between drafts
of the book; cite the draft date alongside the number for precision.

## AI-assisted research

The book documents the contributions of ChatGPT (OpenAI) and Claude
(Anthropic). Mathematical claims should be assessed independently.
