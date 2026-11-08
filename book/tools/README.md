# Book tools

Scripts that generated `book/chapters/*.tex` (Draft 1) from the frozen
papers: Part I Draft 11, Part II Draft 10, Part III Draft 10, Part IV
Draft 6, and the companion paper Draft 8.

1. Compile each frozen draft once, in a scratch directory
   `AUX/<tag>/x.tex` with tags `I10` (Part I Draft 10, the numbering
   used by Part IV and the companion paper), `I` (Part I Draft 11),
   `II`, `III`, `IV`, `W`; put `glossary.tex` in `AUX/`.
2. `python3 convert.py REPO AUX OUT`: prefixes labels per chapter,
   turns typed cross-Part references into `\cref`/`\ref`, turns
   bracketed and `\cite` citations into citations to one bibliography,
   scopes each paper's macros, and moves the literature, notation,
   summary, appendix and acknowledgment blocks. Writes
   `OUT/converted.json` and `OUT/conversion_report.txt`.
3. `python3 assemble.py OUT/converted.json REPO REPO/book`: applies the
   hand-checked fixes for references typed without a "Part" prefix,
   and writes the chapter files.
4. `python3 bib.py OUT/bibs.json REPO/book`: writes the merged
   bibliography. (`bibs.json` is produced by the extraction step in
   the Draft 1 log.)

From Draft 2 on, the chapter files are edited directly; these scripts
document how Draft 1 was produced.
