# Metaplectic Jacquet–Langlands Transfer

Research manuscripts toward a metaplectic Jacquet–Langlands transfer
for division algebras of prime degree.

This is ongoing mathematical research. The manuscripts distinguish
complete proofs, results established in the literature or earlier
parts, conditional statements, and open problems. **The full
metaplectic Jacquet–Langlands correspondence is not claimed to have
been established.**

## The setting

- `K` is a totally imaginary number field containing the `n`th roots
  of unity, with `n` odd.
- `r` is a prime with `gcd(n, r) = 1`.
- `D` is a central division algebra of degree `r` over `K`, ramified
  at a finite set of places `S`.

The series compares two `n`-fold covering groups:

- the cover of `D^×` from the author's corrected 1988 paper on the
  metaplectic analog of Kazhdan's "endoscopic" lifting;
- the Kazhdan–Patterson cover of `GL(r)` with parameter `c_v`, where
  `n` divides `r − 1 + 2 r c_v`.

Both covers sit inside one ambient cover, constructed in Part I.

### Running example

The whole series tests its constructions on one concrete case:
`K = Q(ζ₃)`, `n = 3`, `r = 2`, and the quaternion algebra
`D = (−1, 4 − ζ₃)` over `K`. This algebra is ramified exactly at the
prime above 3 (the wild place, where `b_D = 3` and `c_D = 27`) and at
one prime above 7 (a tame place). Each part has a short "running
example" subsection, and `notes/mjl_running_example.tex` works the
case out in detail across all four parts.

The approach follows the classical trace-formula proof of the
Jacquet–Langlands correspondence. It uses the metaplectic correspondence
of Flicker–Kazhdan (Publ. Math. IHÉS 64, 1986), together with the
corrections of J. Zou (arXiv:2209.05852).

## The manuscripts

| Part | Title | Current draft |
|------|-------|---------------|
| I   | Local matching and a global transfer under elliptic-support conditions | Draft 8 |
| II  | Matching of arbitrary functions and an improved global transfer | Draft 8 |
| III | The division-algebra side and its local character transform | Draft 9 |
| IV  | Local power maps, toral positivity, and conditional global comparison | Concluding Draft 6 |

Each part's full title begins *"A metaplectic Jacquet–Langlands
transfer for division algebras of prime degree"*.

### Part I

- Construction of the covers and of the identification of covered tori.
- Good elements, including at places dividing `n`.
- Matching of regular-supported test functions, with sign `(−1)^(r−1)`.
- A simple trace-formula comparison of the covered inner form with the
  covered `GL(r)`.
- A global transfer ("Theorem C") under a hypothesis `(H_D)`.

### Part II

- Matching of arbitrary genuine test functions, including germs at the
  center.
- A strengthened global transfer ("Theorem C′") under a weaker
  hypothesis `(H_D′)`.

### Part III

- A unitary transform `L_D` between class functions on `D^×` and genuine
  class functions on its cover, with constant `b_D = |n|^(−(r−1)/2)`.
- At places not dividing `n`, `L_D` maps irreducible characters
  bijectively to genuine irreducible characters.
- At places dividing `n`: the cover does not split there, and the
  paper gives a divisibility test with `c_D = |n|^(−(r²−1)/2)`.
- An orbital-integral transfer, and local-to-global results for `n`th
  powers modulo scalars.

### Part IV

- **Cocycles.** Reconciliation of the cocycle conventions of Part I
  and Flicker–Kazhdan.
- **Good elements.** The Flicker–Kazhdan good-element criterion for
  every maximal torus.
- **Power maps.** Kernel, index and Haar modulus of the `n`th-power map
  on étale tori.
- **Global good classes.** A classification of the globally good
  regular elliptic classes.
- **Places dividing `n`, rank two.** Discriminant ratios on every
  quadratic maximal torus, and a toral positivity criterion. The
  companion note `mjl_rank2_wild_toral_positivity_note` proves toral
  positivity for all quadratic tori, at every place dividing `n` and
  for every odd `n`.
- **Positivity.** Integrality of `L_D` at places dividing `n` is
  equivalent to positive definiteness of every transformed irreducible
  character.
- **Ordinary versus covered `D^×`.** A conditional global comparison,
  with an explicit normalization factor.

### Companion paper: the rank-two wild case

`part-IV/mjl_rank2_wild_draftK` (*Wild-place metaplectic character
transfer in degree two: toral positivity and the nonabelian gluing
problem*) is a standalone paper on the open local problem for
quaternion algebras. Draft 0 set the problem up; Drafts 1-4 (November
2026, written by Claude, refereed by ChatGPT) prove:

- **Target A** (the running example's wild place): `L_D·1` is the
  character of a single genuine irreducible representation of dimension
  27, whose restriction to the pro-3 part is induced from an explicit
  character of the covered third congruence subgroup. Label [P^c]: the
  proof uses four exhaustive finite computations (scripts in
  `part-IV/scripts/`, exact arithmetic only); the one previously sampled
  step, hypothesis (H1), has a hand proof since Draft 2.
- **Part of Target B**: the same holds for every irreducible
  representation of `D^×` trivial on the third congruence subgroup
  and all its norm twists (levels zero, one and two); for an arbitrary
  row there is a reduction to the pro-3 Sylow subgroup; levels three
  and higher are open.
- **Part of Target C**: the p-th power identity and the
  multiplicativity of the canonical star section on the 2d-th
  congruence subgroup hold for every odd prime p and every field
  containing the p-th roots of unity.

Each draft has a revision log (`mjl_rank2_wild_revision_log_draftK`);
ChatGPT's referee reports on Drafts 1-5 are the files
`mjl_rank2_wild_draftK_referee_report_chatgpt.md`. Current draft: 6.

### Main open problems

- **Integrality of `L_D` at places dividing `n`.** It is open whether
  `L_D` maps irreducible characters to irreducible genuine characters
  there in general. For the running example (`r = 2`, `n = 3`,
  `F = Q_3(zeta_3)`) the companion paper settles the trivial character and
  all rows trivial on the third congruence subgroup; rows of higher
  level, and other `p` and `F`, remain open.
- **The full comparison of `D^×` with its cover.** The comparison is
  proved only conditionally. What is missing is matching at the places
  where `D` splits and at the complex places.
- **Removing auxiliary hypotheses.** The support and packet hypotheses
  used in Parts I–II should eventually be removed.

## Repository layout

```
part-I/     Part I drafts (.tex, .pdf) and revision logs
part-II/    Part II drafts and revision logs
part-III/   Part III drafts and revision logs
part-IV/    Part IV drafts, revision logs, referee reports, the
            rank-two toral positivity note, and the rank-two
            companion paper (mjl_rank2_wild_draftK) with its
            verification scripts in part-IV/scripts/
notes/      Supporting notes, including the running example
software/   Supporting code (MIT License)
```

### File naming

- **Drafts:** `mjl_partN_draftK.tex`, with the compiled
  `mjl_partN_draftK.pdf`. Earlier drafts are kept for reference; the
  highest draft number is current.
- **Revision logs:** `mjl_partN_revision_log_draftK` (`.tex`, `.pdf`
  or `.md`). They record changes, decisions, reference checks, and
  responses to referee reports. Drafting history is kept in the logs,
  not in the papers.
- **Referee reports:** `*_referee_report_claude` (`.tex` and `.pdf`).

### Status labels in the manuscripts

| Label | Meaning |
|-------|---------|
| **[P]** | Proved in the paper |
| **[E]** | Established in the literature or an earlier part |
| **[O]** | Proof outlined but not fully established |
| **[C]** | Conjectural, or conditional on stated unproved hypotheses |

## Building

Every manuscript is a single self-contained LaTeX file. To build one:

```bash
cd part-IV
pdflatex mjl_part4_draft5.tex
pdflatex mjl_part4_draft5.tex   # second pass for cross-references
```

## Software

- `software/toral_coefficient_check.py` is an independent check of
  the coefficient formulas in the rank-two toral positivity note.
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

Drafts are written and refereed with AI assistance:

- ChatGPT (OpenAI) and Claude (Anthropic) have each drafted and
  refereed parts of the series.
- The referee reports and the responses to them are in the repository.
- Each referee report states which sources were checked against
  originals, and which were not.

Independent human review is the next step. Comments, corrections and
referee reports are welcome through GitHub Issues.

## Licensing

- **Manuscripts:** the research manuscripts, PDFs and original
  explanatory material are licensed under Creative Commons Attribution
  4.0 International (CC BY 4.0).
- **Software:** software in `software/` is licensed under the MIT
  License.
- **Third-party works:** these remain subject to their own licenses and
  are not relicensed by this repository. In particular, previously
  published articles by the author, and revised versions of them, are
  **not** included here, and nothing here relicenses them.

## Citation

When citing a result, identify the part, draft number, and date, for
example: *Part IV, Draft 6 (November 8, 2026), Theorem 6.2*.
Theorem numbers can change between drafts.

## AI-assisted research

The manuscripts document the contributions of ChatGPT (OpenAI) and
Claude (Anthropic). Mathematical claims should be assessed
independently.
