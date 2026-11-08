#!/usr/bin/env python3
"""Assemble the book from converted.json (output of convert.py).

Usage: python3 assemble.py CONVERTED_JSON REPO_DIR BOOK_DIR
Writes BOOK_DIR/chapters/*.tex and BOOK_DIR/mjl_book_draft1.tex.
"""
import json, re, sys, os

CONV, REPO, BOOK = sys.argv[1:4]
d = json.load(open(CONV))
ch, moved, macros, abstracts, gloss = d['chapters'], d['moved'], d['macros'], d['abstracts'], d['glossary']
os.makedirs(os.path.join(BOOK, 'chapters'), exist_ok=True)
log = []

def fix(tag, pairs, where=None):
    tgt = ch if where is None else where
    for a, b in pairs:
        n = tgt[tag].count(a)
        if n == 0:
            raise SystemExit('fix not found in %s: %r' % (tag, a))
        tgt[tag] = tgt[tag].replace(a, b)
        log.append('%s: %d x %r -> %r' % (tag, n, a, b))

# ------------------------------------------------ hand-checked fixes
fix('I', [('its tame irreducible-character theorem (Theorem~7.6)',
           'its tame irreducible-character theorem (\\cref{III:thm:tame-transfer})')])
fix('II', [
    ('Thm.~6.5 (Theorem~B:', '\\cref{I:thm:easy} (Theorem~B:'),
    ('Prop.~6.6 (orbital integrals', '\\cref{I:prop:germ} (orbital integrals'),
    ('Lemma~6.10 (regular support)', '\\cref{I:lem:Aprops} (regular support)'),
    ('Def.~8.5, Thm.~8.6 (comparison)', '\\cref{I:def:globalpairs}, \\cref{I:thm:comparison} (comparison)'),
    ('Prop.~9.6 (packet identity)', '\\cref{I:prop:packet} (packet identity)'),
    ('Def.~9.9, Thm.~9.11 (Theorem~C,', '\\cref{I:def:HD}, \\cref{I:thm:transfer} (Theorem~C,'),
    ('Thm.~9.12, Rem.~9.13 (converse, (H))', '\\cref{I:thm:converse}, \\cref{I:rem:H} (converse, (H))'),
    ('Lemma~9.8 (cancellation)', '\\cref{I:lem:cancel} (cancellation)'),
    ('\\S10, items (D1)--(D4) &', '\\S\\ref{I:sec:deferred}, items (D1)--(D4) &'),
    ('transport (\\S3)}', 'transport (\\S\\ref{II:sec:center})}'),
    ('matching, Lemmas~6.4, 6.10}', 'matching, \\cref{I:lem:transported,I:lem:Aprops}}'),
    ('$f_{\\St}(1)=d(\\St)$\\\\ (\\S5.1)}', '$f_{\\St}(1)=d(\\St)$\\\\ (\\S\\ref{II:subsec:linear})}'),
    ('packet identity (\\S6.1--6.2)}', 'packet identity (\\S\\S\\ref{II:subsec:uadm}--\\ref{II:subsec:packet2})}'),
    ('\\item \\emph{Admissible functions} (\\S6.3).', '\\item \\emph{Admissible functions} (\\S\\ref{I:subsec:transported}).'),
    ('\\item \\emph{Lemma~6.4.}', '\\item \\emph{\\Cref{I:lem:transported}.}'),
    ('\\item \\emph{Theorem~6.5.}', '\\item \\emph{\\Cref{I:thm:easy}.}'),
    ('\\item \\emph{Proposition~6.6.}', '\\item \\emph{\\Cref{I:prop:germ}.}'),
    ('\\item \\emph{Lemma~6.8(b)}', '\\item \\emph{\\Cref{I:lem:Asub}(b)}'),
    ('\\item \\emph{Lemma~6.10.}', '\\item \\emph{\\Cref{I:lem:Aprops}.}'),
    ('\\emph{Lemma~6.12.} Traces', '\\emph{\\Cref{I:lem:traceOI}.} Traces'),
    ('\\item \\emph{Proposition~8.1.}', '\\item \\emph{\\Cref{I:prop:geomD}.}'),
    ('\\item \\emph{Proposition~8.2}', '\\item \\emph{\\Cref{I:prop:FKvariant}}'),
    ('\\item \\emph{Theorem~7.6 and Corollary~7.7.}', '\\item \\emph{\\Cref{I:thm:rational} and \\cref{I:cor:rationalbij}.}'),
    ('\\item \\emph{Lemma~9.2.}', '\\item \\emph{\\Cref{I:lem:nusep}.}'),
    ('\\item \\emph{Lemma~9.8 (proof).}', '\\item \\emph{\\Cref{I:lem:cancel} (proof).}'),
    ('(Definition~9.9) and (H) (Theorem~9.12)', '(\\cref{I:def:HD}) and (H) (\\cref{I:thm:converse})'),
])
fix('III', [
    ('there in Proposition~5.5(b),(d).', 'there in \\cref{I:prop:good}(b),(d).'),
    ('The section depends on \\S2 and introduces', 'The section depends on \\S\\ref{III:sec:setting} and introduces'),
    ('The section depends on \\S\\S2--3.', 'The section depends on \\S\\S\\ref{III:sec:setting}--\\ref{III:sec:power}.'),
    ('The section depends on \\S4 and introduces', 'The section depends on \\S\\ref{III:sec:local} and introduces'),
    ('The section depends on \\S\\S2--6,', 'The section depends on \\S\\S\\ref{III:sec:setting}--\\ref{III:sec:adams},'),
    ('The section depends on \\S\\S2 and~5', 'The section depends on \\S\\S\\ref{III:sec:setting} and~\\ref{III:sec:characters}'),
    ('This section depends on \\S\\S2 and~4.', 'This section depends on \\S\\S\\ref{III:sec:setting} and~\\ref{III:sec:local}.'),
    ('The section depends on \\S3 and on global', 'The section depends on \\S\\ref{III:sec:power} and on global'),
    ('The section depends on \\S\\S9--11', 'The section depends on \\S\\S\\ref{III:sec:orbital}--\\ref{III:sec:global-power}'),
])
fix('III', [('a maximal torus $T=E^\\times$ (\\S2).', 'a maximal torus $T=E^\\times$ (\\S\\ref{III:sec:setting}).')], where=moved['gloss'])
fix('IV', [('(Appendix~\\ref{I:app:cusp}, item~(R4);', '(\\S\\ref{I:app:cusp}, item~(R4);')])
fix('W', [
    ('(Definition~2.2, Proposition~2.3);', '(\\cref{I:lem:center}, \\cref{I:prop:restriction});'),
    ('(Proposition~3.1);', '(\\cref{I:prop:comm});'),
    ('(Proposition~3.5(a));', '(\\cref{I:prop:good}(a));'),
    ('(Lemma~3.4);', '(\\cref{I:lem:FcapEn});'),
    ('(Theorem~3.9, Remark~8.1)', '(\\cref{I:thm:ident}, \\cref{I:rem:D2tame})'),
])
for t in ch:
    ch[t] = ch[t].replace('Appendix~\\ref{I:app:', '\\S\\ref{I:app:')

TITLES = {
    'I': 'Local matching and a global transfer under elliptic-support conditions',
    'II': 'Matching of arbitrary functions and an improved global transfer',
    'III': 'The division-algebra side and its local character transform',
    'IV': 'Local power maps, toral positivity, and conditional global comparison',
    'W': 'The wild place in degree two: toral positivity and the nonabelian gluing problem',
}
SOURCE = {
    'I': 'Part~I, Draft~11', 'II': 'Part~II, Draft~10', 'III': 'Part~III, Draft~10',
    'IV': 'Part~IV, concluding Draft~6', 'W': 'the companion paper on the rank-two wild place, Draft~8',
}

def group(tag, text):
    return '\\begingroup\n%% macros of %s\n%s\n%s\n\\endgroup\n' % (SOURCE[tag], macros[tag], text.strip())

def write(name, text):
    open(os.path.join(BOOK, 'chapters', name), 'w').write(text)

# ------------------------------------------------------ chapters 4--8
FILES = {'I': 'ch4_part1', 'II': 'ch5_part2', 'III': 'ch6_part3', 'IV': 'ch7_part4', 'W': 'ch8_wild'}
for t, f in FILES.items():
    body = ch[t].strip()
    head = ('\\chapter{%s}\\label{ch:%s}\n' % (TITLES[t], t) +
            '\\paragraph{Overview.} ' + abstracts[t].strip() + '\n\n' +
            '\\paragraph{Source.} This chapter is %s (November 2026), with references converted to the numbering of this book; see the Preface.\n\n'
            % SOURCE[t])
    write(f + '.tex', '%% Chapter generated from %s by booktools/assemble.py\n' % SOURCE[t] + group(t, head + body))

# ------------------------------------------------------ chapter 2: literature
def retitle(block, old, new):
    assert block.count(old) >= 1, (old, block[:200])
    return block.replace(old, new, 1)

litI = retitle(moved['lit']['I'], '\\section{Literature}', '\\section{The literature of the series}')
litII = retitle(moved['lit']['II'], '\\section{Related work}', '\\section{Work related to \\texorpdfstring{Chapter~\\ref{ch:II}}{Chapter 5}}')
litIII = retitle(moved['lit']['III'], '\\section{Related work}', '\\section{Work related to \\texorpdfstring{Chapter~\\ref{ch:III}}{Chapter 6}}')
litW = retitle(moved['lit']['W'], '\\section{Related literature}', '\\section{Work related to \\texorpdfstring{Chapter~\\ref{ch:W}}{Chapter 8}}')
lit = ('\\chapter{Literature}\\label{ch:lit}\n'
       'This chapter reviews the literature on which the book draws. Section~\\ref{I:sec:lit} reviews the literature of the whole series; '
       'the later sections add what is specific to Chapters~\\ref{ch:II}, \\ref{ch:III} and~\\ref{ch:W}. '
       'Chapter~\\ref{ch:IV} has no separate related-work section; its sources are discussed in its own text.\n\n'
       + group('I', litI) + group('II', litII) + group('III', litIII) + group('W', litW))
write('ch2_literature.tex', lit)

# ------------------------------------------------------ chapter 3: notation
def addendum(block, start, title):
    i = block.index(start)
    return '\\section{%s}' % title + block[i + len(start):]

gI = addendum(moved['gloss']['I'], '\\subsection{Notation specific to Chapter~\\ref{ch:I}}', 'Notation specific to \\texorpdfstring{Chapter~\\ref{ch:I}}{Chapter 4}')
gII = addendum(moved['gloss']['II'], '\\subsection{Notation specific to Chapter~\\ref{ch:II}}', 'Notation specific to \\texorpdfstring{Chapter~\\ref{ch:II}}{Chapter 5}')
gIII = addendum(moved['gloss']['III'], '\\subsection{Notation and terminology specific to Chapter~\\ref{ch:III}}', 'Notation and terminology specific to \\texorpdfstring{Chapter~\\ref{ch:III}}{Chapter 6}')
gIV = retitle(moved['gloss']['IV'], '\\section{Selected glossary}', '\\section{Terminology specific to \\texorpdfstring{Chapter~\\ref{ch:IV}}{Chapter 7}}')
# drop the file's header comments (they contain example LaTeX lines)
gl = gloss[gloss.index('\\subsection{Status labels}'):]
gl = gl.replace('\\subsection{', '\\section{')
notation = ('\\chapter{Notation and glossary}\\label{ch:notation}\\label{I:sec:glossary}\\label{II:sec:glossary}\\label{III:sec:glossary}\n'
            'This chapter collects the notation and conventions of the book. Sections~\\ref{gl:labels}--\\ref{gl:named} hold for every chapter; '
            'they include the status labels (\\S\\ref{gl:labels}) and the cocycle normalization (\\S\\ref{gl:cocycle}). '
            'The remaining sections list the notation specific to individual chapters, with pointers to the definitions. '
            'The chapter proves nothing and can be consulted at any point.\n\n'
            + gl + '\n' + group('I', gI) + group('II', gII) + group('III', gIII) + group('IV', gIV))
write('ch3_notation.tex', notation)

# ------------------------------------------------------ chapter 9: summary
sI = retitle(moved['summary']['I'], '\\section{Summary of results}', '\\section{\\texorpdfstring{Chapter~\\ref{ch:I}}{Chapter 4}: %s}' % TITLES['I'])
sII = retitle(moved['summary']['II'], '\\section*{Summary of results}\\addcontentsline{toc}{section}{Summary of results}', '\\section{\\texorpdfstring{Chapter~\\ref{ch:II}}{Chapter 5}: %s}' % TITLES['II'])
sIII = retitle(moved['summary']['III'], '\\section*{Summary of results}\\addcontentsline{toc}{section}{Summary of results}', '\\section{\\texorpdfstring{Chapter~\\ref{ch:III}}{Chapter 6}: %s}' % TITLES['III'])
sW = retitle(moved['summary']['W'], '\\section{Summary of results}', '\\section{\\texorpdfstring{Chapter~\\ref{ch:W}}{Chapter 8}: %s}' % TITLES['W'])
sIV = ('\\section{\\texorpdfstring{Chapter~\\ref{ch:IV}}{Chapter 7}: %s}\\label{IV:sec:summary}\n' % TITLES['IV'] +
       abstracts['IV'].strip() + '\n\nThe status of each statement is tabulated in \\S\\ref{IV:sec:intro}.\n')
summary = ('\\chapter{Summary of results}\\label{ch:summary}\n'
           'This chapter lists the results of Chapters~\\ref{ch:I}--\\ref{ch:W} with their status labels (\\S\\ref{gl:labels}) and pointers, one section per chapter.\n\n'
           + group('I', sI) + group('II', sII) + group('III', sIII) + group('IV', sIV) + group('W', sW))
write('ch9_summary.tex', summary)

# ------------------------------------------------------ appendix
app = ('\\chapter{Tables and verification scripts for \\texorpdfstring{Chapter~\\ref{ch:W}}{Chapter 8}}\\label{ch:scripts}\n'
       + group('W', moved['appendix']))
write('appA_scripts.tex', app)

# ------------------------------------------------------ preface acknowledgments
acks = '\n\n'.join('\\paragraph{%s.} %s' % ({'I': 'Chapter~\\ref{ch:I}', 'II': 'Chapter~\\ref{ch:II}', 'III': 'Chapter~\\ref{ch:III}',
                                              'IV': 'Chapter~\\ref{ch:IV}', 'W': 'Chapter~\\ref{ch:W}'}[t],
                                             group(t, moved['ack'][t]))
                   for t in ['I', 'II', 'III', 'IV', 'W'])
write('acknowledgments_generated.tex', acks)
open(os.path.join(BOOK, 'assemble_fixes.txt'), 'w').write('\n'.join(log) + '\n')
print('ok', len(log), 'fixes')
